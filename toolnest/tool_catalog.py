"""Human-written content for ToolNest's dedicated tool pages.

The keys are the existing V4 front-end tool identifiers; slugs are public URLs.
Keep the limits here consistent with pdf_tools.py and app.py.
"""
TOOL_PAGES = [
    {
        'key':'compress','slug':'image-compressor','title':'Image Compressor','category':'image','label':'Image tools','glyph':'▧',
        'seo_title':'Free Image Compressor Online | JPEG, PNG & WebP | ToolNest',
        'description':'Compress JPG, PNG and WebP images online for free. Resize large images and download a smaller WebP when possible. No account needed.',
        'lead':'Reduce image file sizes for easier sharing, email attachments and everyday web use.',
        'intro':'ToolNest accepts JPG, PNG and WebP images and attempts to create a smaller WebP image. Large uploads are resized to fit within 2,000 × 2,000 pixels. When the output would be larger, you receive your original file instead.',
        'steps':['Select a JPG, PNG or WebP image up to 8 MB.','Choose Compress & download to optimize the image.','Open your downloaded file and compare its size and appearance.'],
        'tips':['The downloaded format may be WebP even when you uploaded a JPG or PNG.','Already-small, optimized images may not get any smaller.','Compression can soften fine details; always review images intended for print.'],
        'faqs':[('Will my image quality change?','Possibly. The compressor uses lossy WebP settings, which can reduce very fine details.'),('What if the image cannot be made smaller?','ToolNest returns the original file rather than a larger version.'),('Which images are supported?','JPG, PNG and WebP images up to 8 MB and 25 megapixels.')],
        'related':['pdf-compress','pdf-create','qr']
    },
    {
        'key':'qr','slug':'qr-code-generator','title':'QR Code Generator','category':'image','label':'Image tools','glyph':'▦',
        'seo_title':'Free QR Code Generator for Links & Text | ToolNest',
        'description':'Generate and download a QR code PNG for a link or short text. Free online QR code generator with no sign-up.',
        'lead':'Turn a web link or short message into a downloadable QR code.',
        'intro':'QR codes make it easier to share a website address or a short piece of text. Paste your content, generate a code and scan it with another device to make sure it leads to the expected destination.',
        'steps':['Enter a complete URL or a short text message.','Select Generate & download QR to save a PNG.','Scan the image with a phone camera before printing or sharing it.'],
        'tips':['For website links, include https:// so scanners recognize the link correctly.','Test the QR code at the actual size you plan to print.','Keep the code clear and leave some white space around it.'],
        'faqs':[('Do these QR codes expire?','The code itself does not expire, but a destination website can be changed or removed.'),('Can I use this QR code on a flyer?','Yes. Check that it remains readable at your intended print size.'),('What is the maximum input length?','This version accepts up to 2,000 characters.')],
        'related':['image-compressor','password','word']
    },
    {
        'key':'word','slug':'word-counter','title':'Word Counter','category':'text','label':'Text & utilities','glyph':'≡',
        'seo_title':'Free Word & Character Counter Online | ToolNest',
        'description':'Count words, characters and sentences instantly as you type. Free online word counter that runs in your browser.',
        'lead':'Check word count, characters and sentences while you write.',
        'intro':'Paste an assignment, product description or social post into the box and see counts update as you type. Counting happens in your browser; your text does not need to be uploaded for this tool.',
        'steps':['Paste or type text in the editor.','Read the live word, character and sentence totals.','Edit your text and watch the totals update immediately.'],
        'tips':['Words are counted using whitespace separation, so unusual punctuation can affect the total.','The character count includes spaces and line breaks.','Sentence detection is approximate, especially around abbreviations.'],
        'faqs':[('Does the counter upload my writing?','No. This word counter runs locally in your browser.'),('Are spaces included in the character count?','Yes, spaces and line breaks count as characters.'),('Are sentence totals always exact?','No. Sentence boundaries can be ambiguous, so treat the result as an estimate.')],
        'related':['text-case-converter','password','pdf-to-text']
    },
    {
        'key':'password','slug':'password-generator','title':'Password Generator','category':'text','label':'Text & utilities','glyph':'✳',
        'seo_title':'Free Random Password Generator Online | ToolNest',
        'description':'Generate random passwords of 8 to 64 characters in your browser. Choose numbers and symbols and copy your result.',
        'lead':'Create random passwords without sending them to ToolNest servers.',
        'intro':'Choose a length and whether to include numbers and symbols. The generator uses your browser’s cryptographic randomness to produce the result locally.',
        'steps':['Choose a password length between 8 and 64 characters.','Select whether to include numbers and symbols.','Generate a password and copy it to your password manager.'],
        'tips':['Use a unique password for every account.','Longer passwords are generally harder to guess.','Avoid pasting real account passwords into online forms or chat conversations.'],
        'faqs':[('Does ToolNest store generated passwords?','No. Generation happens in your browser and this app does not send generated passwords to its server.'),('Does every password contain every selected character type?','Not necessarily. Options set the eligible character set; an individual password may not include every type.'),('How long can a password be?','This generator supports lengths from 8 to 64 characters.')],
        'related':['word-counter','text-case-converter','qr']
    },
    {
        'key':'case','slug':'text-case-converter','title':'Text Case Converter','category':'text','label':'Text & utilities','glyph':'Aa',
        'seo_title':'Free Uppercase, Lowercase & Title Case Converter | ToolNest',
        'description':'Convert text to UPPERCASE, lowercase, Title Case or Sentence case instantly. Free text case converter, no sign-up.',
        'lead':'Fix capitalization in a few clicks without retyping text.',
        'intro':'Text Case Converter is handy when formatting headlines, notes, captions or copied documents. It transforms the text locally in your browser so you can copy the version you need.',
        'steps':['Paste the text you want to change.','Choose UPPERCASE, lowercase, Title Case or Sentence case.','Copy the converted result and paste it wherever you need it.'],
        'tips':['Title Case capitalizes each word; it does not follow every editorial style guide.','Sentence case applies simple punctuation rules and may need proofreading.','Always check names, acronyms and unusual spelling after conversion.'],
        'faqs':[('Can I convert multiple lines of text?','Yes. Paste your entire text and choose a conversion.'),('Is the converted text uploaded?','No. This tool runs in your browser.'),('Does Sentence case understand grammar?','It uses basic capitalization patterns rather than a grammar engine.')],
        'related':['word-counter','pdf-to-text','password']
    },
    {
        'key':'pdf-merge','slug':'merge-pdf','title':'Merge PDF','category':'pdf','label':'PDF tools','glyph':'⊕',
        'seo_title':'Merge PDF Files Online for Free | ToolNest',
        'description':'Combine 2 to 20 PDF files into one document online. Free PDF merge tool with no account required.',
        'lead':'Combine multiple PDF documents into a single file.',
        'intro':'Merge PDF puts uploaded documents together in your selected order. It is useful for assembling reports, proposals, handouts and other multi-file documents without editing their individual pages.',
        'steps':['Select 2 to 20 PDF files together in the file picker.','Check your selection order before proceeding.','Select Merge & download and review the combined PDF.'],
        'tips':['Choose multiple files in one file-picker action; choosing again replaces the prior selection.','The combined document is limited to 150 pages and uploads must total 30 MB or less.','Keep a copy of each original file in case you need to rearrange pages.'],
        'faqs':[('How many PDFs can I merge?','Select between 2 and 20 PDFs, with no more than 150 pages in total.'),('Can I merge password-protected PDFs?','Not in this version. Remove protection only if you are authorized to do so.'),('Does the tool let me rearrange individual pages?','No. It joins each uploaded PDF in file selection order.')],
        'related':['split-pdf','compress-pdf','rotate-pdf']
    },
    {
        'key':'pdf-split','slug':'split-pdf','title':'Split / Extract PDF','category':'pdf','label':'PDF tools','glyph':'✂',
        'seo_title':'Split PDF & Extract Pages Online for Free | ToolNest',
        'description':'Extract selected pages from a PDF by page number or range. Free PDF splitting tool with no sign-up.',
        'lead':'Keep only the pages you need from a larger PDF.',
        'intro':'Extract selected PDF pages into a new document. Enter individual page numbers or ranges, such as 1,3-5, to pull exactly the sections you want without altering your original file.',
        'steps':['Upload a PDF containing the pages you want.','Enter numbers such as 2,4-6, or leave the field blank for all pages.','Select Extract & download and check the resulting PDF.'],
        'tips':['Page numbers start at 1, not 0.','Separate pages with commas and use a hyphen for a range.','A blank selection keeps all pages rather than splitting them into separate files.'],
        'faqs':[('Can I extract non-consecutive pages?','Yes. Enter a selection such as 1,3,7-9.'),('Does this create a separate PDF for each page?','No. The selected pages are combined into one downloaded PDF.'),('Will it change my original document?','No. The tool creates a new output file.')],
        'related':['merge-pdf','rotate-pdf','pdf-to-jpg']
    },
    {
        'key':'pdf-compress','slug':'compress-pdf','title':'Compress PDF','category':'pdf','label':'PDF tools','glyph':'▤',
        'seo_title':'Compress PDF Online — Light, Balanced & Strong | ToolNest',
        'description':'Try free online PDF compression with Light, Balanced and Strong modes. Reduce large image-heavy PDFs when possible. No account needed.',
        'lead':'Reduce PDF size for sharing and attachments, with adjustable image quality.',
        'intro':'Choose Light to preserve image appearance, Balanced for a middle ground or Strong for a smaller image-heavy PDF. Results vary: some documents are already optimized, and files with many high-resolution photos take longer to process.',
        'steps':['Select one PDF under 14 MB and up to 150 pages.','Choose Light, Balanced or Strong compression.','Download the output and check text, images and file size.'],
        'tips':['Strong mode can soften photos and fine graphics.','Text-based PDFs may barely change size; image-rich PDFs often have more room to shrink.','Make sure your compressed file is readable before sending it to others.'],
        'faqs':[('Which compression mode should I pick?','Start with Balanced, then compare Light or Strong if needed.'),('Why did my PDF not get smaller?','Some PDFs are already optimized; ToolNest avoids returning an output larger than the original.'),('What is the file limit?','PDF compression is currently limited to 14 MB per uploaded document on this hosting setup.')],
        'related':['merge-pdf','image-compressor','pdf-to-jpg']
    },
    {
        'key':'pdf-rotate','slug':'rotate-pdf','title':'Rotate PDF','category':'pdf','label':'PDF tools','glyph':'↻',
        'seo_title':'Rotate PDF Pages 90°, 180° or 270° Online | ToolNest',
        'description':'Rotate all pages of a PDF by 90, 180 or 270 degrees online. Free PDF rotation with no registration required.',
        'lead':'Fix sideways or upside-down PDF pages in one step.',
        'intro':'Use this tool when a scanned or exported PDF is oriented the wrong way. Choose a rotation angle and create a new PDF with its pages rotated in the same direction.',
        'steps':['Upload your PDF file.','Choose 90°, 180° or 270° clockwise rotation.','Download the updated PDF and confirm the pages read correctly.'],
        'tips':['Rotation affects every page in the document.','For mixed page orientations, extract pages first, rotate groups separately, then merge.','Your original PDF is not modified by this tool.'],
        'faqs':[('Can I rotate just one page?','Not directly. Extract the page first, rotate it, and merge it back if needed.'),('Will rotation remove PDF text?','Rotation normally preserves existing page content; inspect the result to confirm.'),('Which angle turns an upside-down page upright?','Usually 180°, but it depends on the starting orientation.')],
        'related':['split-pdf','merge-pdf','pdf-to-jpg']
    },
    {
        'key':'pdf-images','slug':'pdf-to-jpg','title':'PDF to JPG','category':'pdf','label':'PDF tools','glyph':'▧',
        'seo_title':'Convert PDF Pages to JPG Images Online | ToolNest',
        'description':'Convert selected PDF pages into JPG images and download them in a ZIP file. Free PDF to JPG converter.',
        'lead':'Turn PDF pages into easy-to-share JPG images.',
        'intro':'Export PDF pages as JPG pictures for presentations, previews or content drafts. ToolNest puts the JPG files in a ZIP archive so multiple pages can be downloaded together.',
        'steps':['Upload a PDF and optionally choose pages such as 1-3.','Select Convert to JPG (ZIP).','Download the ZIP and open the JPG images inside.'],
        'tips':['Export up to 30 pages per conversion.','JPG is a raster image format, so exported text is no longer selectable.','Output clarity depends on the PDF and the conversion resolution.'],
        'faqs':[('Why did I download a ZIP?','ZIP bundles the generated JPG files into one download.'),('Can I choose just one PDF page?','Yes. Enter that page number in the optional page selection field.'),('Can I export every page of a large PDF at once?','This version limits JPG exports to 30 selected pages per request.')],
        'related':['images-to-pdf','split-pdf','image-compressor']
    },
    {
        'key':'pdf-create','slug':'images-to-pdf','title':'Images to PDF','category':'pdf','label':'PDF tools','glyph':'▧',
        'seo_title':'Convert JPG, PNG & WebP Images to PDF Free | ToolNest',
        'description':'Combine JPG, PNG and WebP images into a single PDF document. Free images to PDF converter with no account required.',
        'lead':'Combine photos, screenshots and graphics into one PDF.',
        'intro':'Images to PDF helps create a single document from multiple image files. It is useful for bundling screenshots, scanned pages or reference photos before sharing them.',
        'steps':['Select one or more JPG, PNG or WebP images together.','Choose Create PDF to combine them.','Open the resulting PDF and check the page order and readability.'],
        'tips':['Choose all images in one file-picker action, ideally in the desired order.','Image files must be under 25 megapixels each, with uploads totaling 30 MB or less.','Keep original images if you need to edit or reorder them later.'],
        'faqs':[('Can I combine multiple images into one PDF?','Yes. Select up to 20 images in a single upload.'),('Which image formats work?','JPG, PNG and WebP are supported.'),('Will the PDF keep transparent backgrounds?','Images are converted to RGB, so transparency may not be preserved.')],
        'related':['pdf-to-jpg','merge-pdf','image-compressor']
    },
    {
        'key':'pdf-text','slug':'pdf-to-text','title':'PDF to Text','category':'pdf','label':'PDF tools','glyph':'≡',
        'seo_title':'Extract Text from PDF Online for Free | ToolNest',
        'description':'Extract selectable text from a PDF and download a TXT file. Free PDF to text converter; scanned PDFs require OCR.',
        'lead':'Copy the selectable words from a PDF into an editable text file.',
        'intro':'PDF to Text can extract text already embedded in a digital PDF. The result is a plain-text file without the original layout. A scanned PDF made only of pictures needs OCR, which ToolNest does not currently provide.',
        'steps':['Upload a PDF containing selectable text.','Select Extract text to generate a TXT file.','Open the text file and review formatting, line breaks and missing characters.'],
        'tips':['Try selecting text in your PDF viewer before using this tool.','Multi-column layouts and tables may appear out of reading order in plain text.','Scanned images of documents will not become editable text without OCR.'],
        'faqs':[('Can this read a scanned PDF?','No. This version has no optical character recognition (OCR).'),('Will it preserve fonts and page layout?','No. It exports plain text rather than the PDF design.'),('Can I extract text from a password-protected PDF?','Not in this version.')],
        'related':['word-counter','text-case-converter','split-pdf']
    }
]
BY_SLUG = {tool['slug']: tool for tool in TOOL_PAGES}
BY_KEY = {tool['key']: tool for tool in TOOL_PAGES}
