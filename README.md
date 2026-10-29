# FREAK lab — static migration

Futuristic Research in Enigmatic + Aesthetic Knowledges.

The site preserves the original FREAK lab presentation and published content, with native static interactions replacing WordPress plugin execution. Deploy **`public/`** to Hostatom or another static web server. PHP and WordPress are not needed.

## Preview

```sh
python3 -m http.server 8766 --directory public
```

Open `http://localhost:8766/`. Use a web server, rather than opening HTML files directly, so root-relative links and static search work correctly.

## Content and maintenance

- `public/`: committed, deployment-ready website. It contains no PHP or WordPress scripts.
- Root HTML directories: generated source pages, preserving the original URL structure.
- `content/published.json`: published editorial content, custom fields, relationships, and image metadata recovered from WordPress. It excludes drafts, account information, and internal plugin settings.
- `content/original-pages.tar.gz`: frozen public-page markup captured on 29 October 2026. Presentation reference for an offline rebuild; never deployed.
- `assets/`: native interactions, verified styles/fonts, search index, and recovered original images.
- `audit/`: migration, media, content recovery, and verification reports. Never deployed.
- `tools/`: optional local authoring, packaging, and audit utilities. Never deployed.

For a small edit, update the root HTML or `assets/site.*`, then package and verify:

```sh
python3 tools/build.py
python3 tools/verify.py
```

To change recovered descriptions, biographies, or gallery relationships, edit `content/published.json`, then run:

```sh
python3 tools/restore_content.py
python3 tools/finalize.py
python3 tools/build.py
python3 tools/verify.py
```

Authoring/auditing requires the packages in `requirements-authoring.txt`; the deployed site requires none. To reconstruct the complete frozen migration offline, use `python3 tools/rebuild.py`. That replaces generated root HTML from the frozen snapshot and reapplies the editorial content. Preserve any direct HTML edits before doing so.

The capture and media-download scripts are migration tools, not deployment steps. Do not rerun them against the replacement domain expecting a WordPress source.

## Scope and verification

See [AUDIT.md](AUDIT.md) for the findings and verification limits, and [HOSTATOM-DEPLOY.md](HOSTATOM-DEPLOY.md) for preview, cutover, security, and rollback instructions.

The full-resolution originals are used where available. Images absent from the R2 copy are retained locally. No generated upscaling is used.
