# ToolNest V3 — 12 Tools + Professional Layout

## Run on Windows

Open PowerShell **inside this folder** (the one containing app.py, pdf_tools.py and requirements.txt).

```powershell
py -m pip install -r requirements.txt
python app.py
```

Visit http://127.0.0.1:5000

## What's new
- Search, filters (PDF / Images / Text & utilities), improved mobile header and homepage
- About, Privacy Policy, Terms of Use and Contact pages
- /robots.txt, /sitemap.xml, meta descriptions and canonical links
- All **12 V2 tool features preserved**

## IMPORTANT BEFORE PUBLISHING
1. Edit `templates/page.html`: replace the setup notice on the Contact page with **your own real contact method**.
2. Review the Privacy Policy and Terms to reflect your actual data handling, hosting, analytics and ad providers.
3. This is not AdSense approval. A free hosting subdomain may be ineligible for direct AdSense signup.
4. Your tool processing uses RAM and free hosting may have memory, timeout and file-size limits; test real files before sharing publicly.
5. Set `FLASK_DEBUG=0` in production. Gunicorn can serve this app on Linux using: `gunicorn app:app --bind 0.0.0.0:$PORT`.
6. SEO meta and a sitemap don't guarantee Google indexing or traffic.

## Folder warning
Do **not** extract the ZIP into an existing `toolnest` folder and then accidentally run the older outer app.py. Extract to a NEW location and open the folder containing both `app.py` and `pdf_tools.py`.
