# Migration audit — 29 October 2026

The clone was a WordPress HTML export with active plugin scripts, unavailable server endpoints, broken relative links, lazy-loading placeholders, missing fonts, and reduced card thumbnails. Its empty detail pages did not contain the underlying custom-field descriptions.

The migration captures the public original and recovers published editorial fields through the existing Plesk session. WordPress content and the database were not modified. A private export was saved outside website roots; no credentials, drafts, account records, or internal plugin settings are included in the public deployment.

## What is preserved and restored

- 283 captured public pages, plus static search and a custom 404 document: **285 HTML documents** in `public/`.
- All 63 published projects, 55 members, 41 updates, 16 events, 10 talks, and 3 special-interest groups. Existing public archive aliases and pagination remain available.
- Descriptions, biographies, affiliations, publication citations, awards, videos, original gallery images, collaborators, and related-member links recovered from their editorial fields.
- Existing research pages, residency material, and the standalone symposium presentation. Its desktop slide controls and mobile scrolling layout remain intact.
- Original URL paths and presentation styles, with static responsive layouts replacing plugin positioning. This is a content-preserving migration, not a claim that every plugin animation is pixel-identical.

## WordPress dependency removal

The production directory contains no PHP, WordPress installation, plugin scripts, admin interface, WordPress AJAX calls, or database requirement. Native JavaScript supplies project/member filters, update pagination, menus, mobile submenus, tabs, accordions, sliders, image dialogs, and text-only local search.

Styles and fonts required by the original presentation are retained as static assets. Original plugin stylesheets are presentation data only; they execute no WordPress code. Unneeded theme/demo asset requests are removed. Scripts and executable event attributes from recovered editorial HTML are not imported.

## Image resolution and recovery

R2 references are checked against the supplied public bucket. Missing originals were recovered from the original uploads instead of enlarging thumbnails. The deployable package includes only the local images actually referenced by its pages. Gallery links open the original source files; the iSnail image was verified in the browser at **1,600 pixels wide**.

Twelve legacy press and award images were recovered from web archive snapshots of their exact original image URLs. A Medium-hosted source photo was also recovered as an image file after its server rejected a HEAD request. Archive timestamps, provenance, and verified dimensions are recorded in `audit/external-image-map.json`.

**Two historical portrait files remain unavailable**: Alan Archapiraj's embedded portrait and the externally hosted Wares Chancharoen portrait in the IAF update. Their original URLs and the affected pages are listed in `audit/missing-original-images.json`. The site shows readable placeholders and preserves the surrounding editorial text and coverage links. It does not fabricate replacement photographs. Exact visual parity requires those original files.

An additional unreferenced historical attachment, `ท่าน-ว-poster.004.jpeg`, was absent from the original public uploads and R2; it is not requested by the deployment.

Thirty member records have no authored biography/gallery in the available source, or contain only a generic unfilled profile template. Their available name, role, affiliation, portrait, group membership, and contact information are retained. No biography has been invented.

## Verification

`tools/verify.py` checks every production HTML document and its local links, scripts, styles, image references, CSS font/image references, published custom-field text, and substantive authored body text. It also rejects server executables and WordPress service calls in the production directory. Source typography differences and intentionally rendered shortcodes are normalized in text comparisons.

The complete offline reconstruction from the frozen snapshot passed. The generated site passes the local-reference and source-text audit with **zero errors and zero warnings**. Python authoring tools compile, and the native site JavaScript passes syntax checking.

Browser checks covered:

- All eleven homepage filters: visible card counts match the original categories (63 total; Biodigital 19; Cat Space 15; remaining categories verified individually).
- Update pagination, including advancing from items 1–8 to 9–16 on desktop.
- Restored member biography/affiliation and linked profile information.
- Static search and title-first result ordering.
- Original-resolution gallery opening and closing.
- All twelve recovered Jube press/award images loaded without errors at their original 519- or 706-pixel widths.
- Symposium desktop next-slide behavior and mobile scrolling presentation.
- Mobile search/header and nested research navigation at 393 pixels, with no horizontal overflow; desktop layout at 1,587 pixels.

The browser checks are representative interaction tests, not a claim of manual visual inspection of every page. Third-party videos, maps, forms, and external coverage websites remain subject to their providers' availability and policies.

## Hostatom boundary

No live document root, PHP setting, firewall configuration, DNS record, or database has been changed. The deployable output is `public/`; cutover and rollback steps are in `HOSTATOM-DEPLOY.md`.

The included Apache rules need validation on the actual preview domain. nginx does not read `.htaccess`. Deploying to a new directory and disabling PHP are essential; copying static files over an accessible WordPress installation would leave its vulnerable executables behind.
