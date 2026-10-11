# PanPan Marine deployment

Primary canonical domain: `www.panpanmarine.com`. Hosting is GitHub Pages, deployed from the `main` branch of `PanPanTech/panpanmarine.com` by `.github/workflows/pages.yml`. The workflow runs `python build.py`, `python validate.py` and `node --check`, writes `dist/CNAME` and publishes `dist/`.

The previous Sites version (`.openai/hosting.json`) is kept as a fallback until the GitHub Pages version has been verified. A push to GitHub no longer needs a separate Sites deployment.

## Alibaba Cloud DNS (GitHub Pages)

Replace only the website records in the existing `panpanmarine.com` zone. Keep mail and unrelated verification records. Do not change nameservers.

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | panpantech.github.io |

Remove the old Sites records for `@` (162.159.143.30, 172.66.3.26) and `www` (custom-domains.chatgpt.site). The `_openai-site-verification` TXT records can be removed once the Sites version is retired.

After propagation, check the custom domain in the repository's Pages settings, enable Enforce HTTPS, and verify the homepage, equipment routes, enquiry form and sitemap over HTTPS.

## Updates

Run `python build.py`, start `python -m http.server 4173 --directory dist --bind 127.0.0.1`, then run `python validate.py`. Commit and push to `main`; GitHub Actions publishes the site.

## Enquiries

The project-brief form posts to the shared enquiry service `https://inquiry.panpantechnology.com/api/inquiries` with `lead_brand: "PanPan Marine"`; leads go to Feishu and Zoho like the other PanPanTech sites. The service must list `https://panpanmarine.com` and `https://www.panpanmarine.com` as allowed origins. If submission fails, the form shows the brief with download and email-draft options addressed to `panda@panpantechnology.com`.
