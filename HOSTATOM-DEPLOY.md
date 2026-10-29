# Deploy the static FREAK lab site on Hostatom / Plesk

The deployable site is **`public/`**. It is ordinary HTML, CSS, JavaScript, fonts, and images. It does not need WordPress, PHP, a database, Node.js, R2 credentials, or a build service at runtime.

## First deployment

1. Keep the existing WordPress site and its database backed up. Exported public content is also preserved in this repository, but that is not a replacement for a full operational backup.
2. In Plesk Git, connect this repository and choose the reviewed static migration branch (or `main` after its pull request is merged).
3. Deploy to a **new, empty directory**, for example `/freaklab-static`. Do not deploy over the existing `/freaklab.org` WordPress directory. A Git deployment does not reliably remove old WordPress executables.
4. Use a preview subdomain with document root **`/freaklab-static/public`**. Leave the live freaklab.org document root unchanged while reviewing. The committed `public/` directory is ready to serve; no additional deployment command is required.
5. In the preview domain's Hosting Settings, **disable PHP support**. Enable HTTPS and directory access through `index.html`. Keep the ModSecurity firewall enabled.
6. Verify homepage filters, a project gallery, a member biography, search, research groups, archives, and the symposium. Check on both a phone and desktop.
7. When approved, set freaklab.org's document root to `/freaklab-static/public`, retain its certificate/HTTPS redirect, and disable PHP for this domain. This is the live cutover; it has not been performed by this migration.

The `.htaccess` file supplies a static 404 page, response headers, directory-listing protection, and blocks legacy WordPress/PHP routes on Apache. If the domain serves files directly through nginx, ask Hostatom to apply equivalent rules and verify PHP is disabled; nginx does not read `.htaccess`.

## Git updates

Edit the generated HTML and static assets, or update the editorial source and rebuild locally. Commit the updated `public/` output and deploy that commit through Plesk Git. Keep deployment keys scoped to this repository and use a separate hosting system user for this site when Hostatom supports it.

If you want Plesk to regenerate the deployable directory after each Git pull, the optional additional deployment action is:

```sh
python3 tools/build.py
```

This packaging step uses only Python's standard library. It copies the already-generated pages and only the local assets they reference. It does not contact WordPress, R2, or any external service. It is unnecessary when deploying the committed `public/` output.

## Images

Existing R2 images continue to use the supplied public bucket URL. Original images missing from that bucket were recovered from the original WordPress uploads and are served from `public/assets/media/`. Do not omit that directory when deploying. No image was enlarged to invent resolution. Detail-page galleries link to their original files.

The `r2.cloudflarestorage.com` S3 endpoint is for authenticated storage operations and is not used in public pages. No storage keys are required or embedded.

## Retire WordPress after cutover

After the static site has been accepted, retain a private backup and ask Hostatom to disable public access to the old WordPress directory and any staging copies. Leaving a vulnerable WordPress installation accessible under another domain or path would retain its attack surface. Check sibling sites sharing the same system user as well.

Do not delete the old site or database until the backup and rollback path have been verified.

## Rollback

Restore the previous document root and its original PHP settings if a live cutover needs to be reversed. The migration has not modified WordPress content or its database. During recovery, a published-content export was written outside all website roots at `/var/www/vhosts/henryandpartners.com/private/freaklab-public-content-20261029.json`; it is not served by this static site.
