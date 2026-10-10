"""PDF endpoints. Compression may use short-lived temporary files, deleted after processing."""
import io
import zipfile
import os
import tempfile
import gc
import fitz
from flask import Blueprint, request, jsonify, send_file
from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError
from PIL import Image, UnidentifiedImageError

pdf_bp = Blueprint('pdf', __name__)
MAX_PDF_PAGES = 150
MAX_UPLOAD_BYTES = 30 * 1024 * 1024


def error(message, code=400):
    return jsonify(error=message), code


def uploaded(key='files'):
    files = [f for f in request.files.getlist(key) if f.filename]
    if not files:
        raise ValueError('Choose at least one file.')
    if len(files) > 20:
        raise ValueError('Select 20 files or fewer.')
    items = []
    total = 0
    for f in files:
        raw = f.read(MAX_UPLOAD_BYTES + 1)
        total += len(raw)
        if total > MAX_UPLOAD_BYTES:
            raise ValueError('Combined upload must be 30 MB or less.')
        items.append(raw)
    return items


def readers():
    docs = []
    for raw in uploaded():
        if not raw.startswith(b'%PDF-'):
            raise ValueError('Only valid PDF files are supported.')
        try:
            doc = PdfReader(io.BytesIO(raw), strict=False)
            if doc.is_encrypted:
                raise ValueError('Password-protected PDFs are not supported.')
            if len(doc.pages) > MAX_PDF_PAGES:
                raise ValueError('A PDF cannot exceed 150 pages.')
            docs.append(doc)
        except (PdfReadError, OSError, KeyError) as exc:
            raise ValueError('The PDF is invalid or cannot be read.') from exc
    return docs


def pdf_response(writer, name):
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return send_file(output, mimetype='application/pdf', as_attachment=True, download_name=name)


def range_pages(raw, limit):
    if not raw.strip():
        return list(range(limit))
    numbers = []
    for chunk in raw.replace(' ', '').split(','):
        if not chunk:
            raise ValueError('Use page numbers like 1,3-5.')
        bits = chunk.split('-')
        try:
            if len(bits) == 1:
                first = last = int(bits[0])
            elif len(bits) == 2:
                first, last = map(int, bits)
            else:
                raise ValueError()
        except ValueError:
            raise ValueError('Use page numbers like 1,3-5.')
        if first < 1 or last > limit or first > last:
            raise ValueError(f'Page selection must be between 1 and {limit}.')
        numbers.extend(range(first-1, last))
    if len(numbers) > MAX_PDF_PAGES:
        raise ValueError('Too many selected pages.')
    return numbers




def smart_compress():
    """Compress one PDF, avoiding full-document rasterization.

    Uses sequential image replacement and periodic saves so decoded images
    are not all retained at once. Output may be returned unchanged when
    no smaller result is achievable. Does not promise every PDF will fit RAM.
    """
    files = uploaded()
    if len(files) != 1:
        raise ValueError('Select exactly one PDF.')
    raw = files[0]
    if not raw.startswith(b'%PDF-'):
        raise ValueError('Only PDF files are supported.')

    mode = request.form.get('compression_level', 'balanced')
    if mode not in ('light', 'balanced', 'strong'):
        raise ValueError('Invalid compression level.')

    # A conservative ceiling for low-memory free hosting. Can be changed
    # using PDF_COMPRESS_MAX_MB in Render environment settings.
    limit_mb = int(os.environ.get('PDF_COMPRESS_MAX_MB', '14'))
    if len(raw) > limit_mb * 1024 * 1024:
        raise ValueError(f'For reliable processing, use a PDF under {limit_mb} MB.')

    settings = {
        'light':    {'quality': 82, 'max_dim': 2200},
        'balanced': {'quality': 62, 'max_dim': 1700},
        'strong':   {'quality': 45, 'max_dim': 1350},
    }[mode]
    paths = []
    pdf = None
    try:
        pdf = fitz.open(stream=raw, filetype='pdf')
        if pdf.needs_pass:
            raise ValueError('Password-protected PDFs are not supported.')
        if len(pdf) > MAX_PDF_PAGES:
            raise ValueError(f'PDFs must have {MAX_PDF_PAGES} pages or fewer.')
        already_seen = set()
        replacements_since_save = 0
        for page_number in range(len(pdf)):
            # Find images without rendering entire pages.
            for image_info in pdf[page_number].get_images(full=True):
                xref = image_info[0]
                if xref in already_seen:
                    continue
                already_seen.add(xref)
                if mode == 'light':
                    continue
                try:
                    info = pdf.extract_image(xref)
                    original_image = info['image']
                    with Image.open(io.BytesIO(original_image)) as img:
                        width, height = img.size
                        if width * height > 14_000_000 or width < 200 or height < 200:
                            continue
                        # Preserve images with transparency or masks rather
                        # than potentially changing appearance when flattened.
                        if img.mode not in ('RGB', 'L') or image_info[1]:
                            continue
                        img.thumbnail((settings['max_dim'], settings['max_dim']))
                        output = io.BytesIO()
                        img.save(output, format='JPEG', quality=settings['quality'], optimize=True)
                        new_image = output.getvalue()
                    if len(new_image) < len(original_image) * 0.92:
                        pdf[page_number].replace_image(xref, stream=new_image)
                        replacements_since_save += 1
                    del info, original_image
                except (ValueError, OSError, RuntimeError, TypeError):
                    # Some image types cannot safely be replaced. Leave intact.
                    continue

                # Periodically save and reopen to release old image versions.
                if replacements_since_save >= 7:
                    fd, temp_path = tempfile.mkstemp(prefix='toolnest-', suffix='.pdf')
                    os.close(fd)
                    paths.append(temp_path)
                    pdf.save(temp_path, garbage=3, deflate=True, use_objstms=1)
                    pdf.close()
                    pdf = fitz.open(temp_path)
                    replacements_since_save = 0
                    gc.collect()

        output = io.BytesIO()
        pdf.save(output, garbage=3, deflate=True, use_objstms=1)
        result = output.getvalue()
        if len(result) >= len(raw):
            result = raw
        return send_file(
            io.BytesIO(result), mimetype='application/pdf',
            as_attachment=True, download_name='optimized.pdf'
        )
    finally:
        if pdf is not None:
            pdf.close()
        for path in paths:
            try:
                os.remove(path)
            except OSError:
                pass


@pdf_bp.post('/api/pdf/<action>')
def process_pdf(action):
    try:
        if action == 'images-to-pdf':
            raw_images = uploaded()
            pictures = []
            try:
                for raw in raw_images:
                    with Image.open(io.BytesIO(raw)) as img:
                        if img.format not in ('PNG', 'JPEG', 'WEBP') or img.width * img.height > 25_000_000:
                            raise ValueError('Use PNG, JPG or WebP images under 25 megapixels.')
                        img.load()
                        pictures.append(img.convert('RGB'))
                out = io.BytesIO()
                pictures[0].save(out, format='PDF', save_all=True, append_images=pictures[1:], resolution=100)
                out.seek(0)
                return send_file(out, mimetype='application/pdf', as_attachment=True, download_name='images.pdf')
            finally:
                for pic in pictures:
                    pic.close()
        if action == 'pdf-to-jpg':
            import fitz
            raw = uploaded()[0]
            if not raw.startswith(b'%PDF-'):
                raise ValueError('Only PDF files are supported.')
            output = io.BytesIO()
            with fitz.open(stream=raw, filetype='pdf') as doc:
                if doc.needs_pass:
                    raise ValueError('Password-protected PDFs are not supported.')
                if len(doc) > MAX_PDF_PAGES:
                    raise ValueError('A PDF cannot exceed 150 pages.')
                indices = range_pages(request.form.get('pages',''),len(doc))
                if len(indices) > 30:
                    raise ValueError('Export up to 30 pages at a time.')
                with zipfile.ZipFile(output,'w', zipfile.ZIP_DEFLATED) as z:
                    for idx in indices:
                        pix = doc[idx].get_pixmap(matrix=fitz.Matrix(1.3,1.3), colorspace=fitz.csRGB, alpha=False)
                        z.writestr(f'page-{idx+1}.jpg',pix.tobytes('jpeg', jpg_quality=80))
            output.seek(0)
            return send_file(output, mimetype='application/zip', as_attachment=True, download_name='pdf-pages.zip')
        if action == 'compress':
            return smart_compress()
        docs = readers()
        if action == 'merge':
            if len(docs)<2:
                raise ValueError('Choose at least two PDFs to merge.')
            if sum(len(d.pages) for d in docs)>MAX_PDF_PAGES:
                raise ValueError('Total must be 150 pages or fewer.')
            writer = PdfWriter()
            for doc in docs:
                for page in doc.pages:
                    writer.add_page(page)
            return pdf_response(writer,'merged.pdf')
        if len(docs)!=1:
            raise ValueError('Select exactly one PDF.')
        doc = docs[0]
        if action == 'split':
            indices = range_pages(request.form.get('pages',''),len(doc.pages))
            writer = PdfWriter()
            for i in indices:
                writer.add_page(doc.pages[i])
            return pdf_response(writer,'selected-pages.pdf')
        if action == 'rotate':
            angle = int(request.form.get('angle','90'))
            if angle not in (90,180,270):
                raise ValueError('Choose 90, 180 or 270 degrees.')
            writer = PdfWriter()
            for page in doc.pages:
                writer.add_page(page)
                writer.pages[-1].rotate(angle)
            return pdf_response(writer,'rotated.pdf')
        if action == 'pdf-to-text':
            contents = '\n\n'.join(f'--- PAGE {i+1} ---\n{page.extract_text() or ""}' for i,page in enumerate(doc.pages))
            data = io.BytesIO(contents.encode('utf-8'))
            return send_file(data, mimetype='text/plain; charset=utf-8', as_attachment=True, download_name='extracted-text.txt')
        return error('Unknown PDF operation.',404)
    except (ValueError, PdfReadError, UnidentifiedImageError, OSError, TypeError, IndexError, KeyError) as exc:
        return error(str(exc) or 'The file could not be processed.')
