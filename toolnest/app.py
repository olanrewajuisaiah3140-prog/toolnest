import io
import os
from flask import Flask, render_template, request, send_file, jsonify, Response, url_for, send_from_directory
from PIL import Image, UnidentifiedImageError
import qrcode

from pdf_tools import pdf_bp
from tool_catalog import TOOL_PAGES, BY_SLUG, BY_KEY

SITE_URL = os.environ.get('SITE_URL', 'https://toolnest-x6cl.onrender.com').rstrip('/')

app = Flask(__name__)
app.register_blueprint(pdf_bp)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024

@app.get('/')
def home():
    return render_template('index.html', tools=TOOL_PAGES, site_url=SITE_URL)


@app.get('/<slug>')
def tool_page(slug):
    tool = BY_SLUG.get(slug)
    if tool is None:
        # Return a true 404; do not serve an unrelated generic tool page.
        from flask import abort
        abort(404)
    related = [BY_SLUG[item] if item in BY_SLUG else BY_KEY[item] for item in tool['related']]
    return render_template('tool.html', tool=tool, related=related, site_url=SITE_URL)


@app.get('/googlea67500ad9983a48a.html')
def google_verification():
    # Preserve the Search Console verification file already used for this website.
    return send_from_directory(app.root_path, 'googlea67500ad9983a48a.html')

@app.context_processor
def site_data():
    return {'site_url': SITE_URL}


@app.get('/about')
def about():
    return render_template('page.html', page='about', title='About ToolNest',
        description='Learn about ToolNest, a free collection of PDF, image and text tools.')

@app.get('/privacy')
def privacy():
    return render_template('page.html', page='privacy', title='Privacy Policy',
        description='Learn how ToolNest handles uploads, browser processing and website data.')

@app.get('/terms')
def terms():
    return render_template('page.html', page='terms', title='Terms of Use',
        description='Read the terms for using free ToolNest utilities.')

@app.get('/contact')
def contact():
    return render_template('page.html', page='contact', title='Contact ToolNest',
        description='Find out how to contact the ToolNest team.')

@app.get('/robots.txt')
def robots():
    return Response(f'User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n', mimetype='text/plain')


@app.get('/sitemap.xml')
def sitemap():
    from xml.sax.saxutils import escape
    paths = ['/', '/about', '/privacy', '/terms', '/contact'] + [f"/{tool['slug']}" for tool in TOOL_PAGES]
    urls = ''.join(f'<url><loc>{escape(SITE_URL + path)}</loc></url>' for path in paths)
    return Response('<?xml version="1.0" encoding="UTF-8"?>'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
                    + urls + '</urlset>', mimetype='application/xml')


@app.get('/health')
def health():
    return jsonify(status='ok')

@app.post('/api/qr')
def make_qr():
    data = (request.form.get('data') or '').strip()
    if not data or len(data) > 2000:
        return jsonify(error='Enter 1–2,000 characters.'), 400
    img = qrcode.make(data)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png', as_attachment=True, download_name='toolnest-qr.png')

@app.post('/api/compress')
def compress_image():
    upload = request.files.get('image')
    if not upload or not upload.filename:
        return jsonify(error='Please select an image.'), 400
    try:
        original = upload.read()
        if len(original) > 8 * 1024 * 1024:
            return jsonify(error='Maximum file size is 8 MB.'), 400
        with Image.open(io.BytesIO(original)) as source:
            if source.format not in ('JPEG', 'PNG', 'WEBP'):
                return jsonify(error='Unsupported image format.'), 400
            if source.width * source.height > 25_000_000:
                return jsonify(error='Image dimensions are too large.'), 400
            source.load()
            has_alpha = 'A' in source.getbands() or (
                source.mode == 'P' and 'transparency' in source.info
            )
            img = source.convert('RGBA' if has_alpha else 'RGB')
            img.thumbnail((2000, 2000))
            output = io.BytesIO()
            img.save(output, format='WEBP', quality=55, method=6)
            compressed = output.getvalue()
            if len(compressed) >= len(original):
                mime = {'JPEG':'image/jpeg','PNG':'image/png','WEBP':'image/webp'}[source.format]
                return send_file(io.BytesIO(original), mimetype=mime,
                                 as_attachment=True, download_name=upload.filename)
            return send_file(io.BytesIO(compressed), mimetype='image/webp',
                             as_attachment=True, download_name='toolnest-compressed.webp')
    except (UnidentifiedImageError, OSError, ValueError):
        return jsonify(error='Image processing failed.'), 400

@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['X-Frame-Options'] = 'DENY'
    return response

@app.errorhandler(413)
def file_too_large(_):
    return jsonify(error='Combined upload must be below 30 MB.'), 413

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG') == '1', port=int(os.getenv('PORT', '5000')))
