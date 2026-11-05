# Site source

The HTML pages in the repo root are generated. Edit `build_site.py`, then run:

    python3 _source/build_site.py .

- Spanish is the default language (`page.html`), English is `page-en.html`, Mandarin is `page-zh.html`, Portuguese is `page-pt.html`.
- Mandarin and Portuguese text come from `zh.json` and `pt.json` (English → translation). New English strings without a translation are listed in `zh_missing.json` / `pt_missing.json` after a build.
- `eps2svg.py` and `extract_logo.py` rebuild the logo files from the designer's EPS.

This folder is excluded from the live site by `.vercelignore`.
