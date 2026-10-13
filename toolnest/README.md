# ToolNest V5 — Premium Design Refresh

A nature-inspired visual redesign based on the layout reference, adapted for ToolNest's 12 free utility tools.

## What's new

- Rich dark-green hero with original visual PDF-workspace illustration (HTML/CSS), rounded floating navigation and prominent search field
- Styled category filters, distinct tool cards, three-step guide, polished FAQs and footer
- Redesigned 12 standalone tool pages and About/Privacy/Terms/Contact pages
- Lightweight custom SVG favicon, responsive layout and keyboard focus styles
- Preserved the V4 Smart PDF Compressor (Light / Balanced / Strong) and all tool API endpoints
- Preserved the Google Search Console verification file and sitemap route (17 URLs)

## Safe local installation on Windows

1. **Keep your V4 and previous V5 folders.** Do not overwrite them yet.
2. Extract the **complete** ZIP and open the `toolnest` folder containing `app.py` and `requirements.txt` in VS Code.
3. In VS Code Terminal run `py -m pip install -r requirements.txt`.
4. Run `python app.py`. Visit `http://127.0.0.1:5000`.
5. Check the homepage, search, category filters, `merge-pdf`, `compress-pdf` (especially Strong), and pages such as `/privacy`.
6. Once it works locally, push this version into the **existing** GitHub repository's `toolnest/` folder. Keep the GitHub files within `toolnest/static/` and `toolnest/templates/`. Render can then deploy automatically.

## Apply the small update to a previously working V5

The **update-only** ZIP contains only presentation files:

- `static/style.css` (replace)
- `static/favicon.svg` (add)
- `templates/index.html` (replace)
- `templates/tool.html` (replace)
- `templates/page.html` (replace)

No changes are needed in `app.py`, `pdf_tools.py`, `tool_catalog.py`, `requirements.txt` or `static/script.js` **if your existing project is already V5**. If your working project is still V4, use the complete V5 project instead of update-only.

## Notes

- This version changes the **design**, not the underlying compression algorithms or existing file-processing limits.
- The demo file-processing interface in the homepage hero is decorative: actual tools function on their own tool pages.
- It does not add analytics, advertisements or new trackers.
- Hosting resource limits can still affect large PDF uploads. Test live processing after deployment.
- The free Render subdomain and Search Console verification are preserved; search indexing and AdSense approval are not guaranteed.
