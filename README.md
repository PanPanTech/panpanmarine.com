# PanPan Marine

English B2B website for industrial underwater inspection and maintenance equipment.

- Brand: PanPan Marine, a PanPanTech brand
- Website operator: Guangzhou PanPanTech Co., Ltd.
- Primary domain: https://www.panpanmarine.com
- Enquiries: panda@panpantechnology.com
- Source repository: https://github.com/PanPanTech/panpanmarine.com

The site contains 43 content routes: seven application pages, five equipment models (each with a printable spec sheet), a side-by-side comparison page, manufacturer case studies, support, a resources hub, company information, a quote form and legal pages, plus a blog hub, three topic pages and six buying guides. It also publishes `llms.txt`, `sitemap.xml` (with `lastmod`) and an RSS feed.

## Build and preview

Python 3 standard library only; no package installation is required.

Run `python build.py`, then `python -m http.server 4173 --directory dist --bind 127.0.0.1`. In another terminal, run `python validate.py` and `node --check dist/assets/site.js`.

`config.json` controls the brand, operator, email and canonical origin. Optional keys are rendered only when filled in:

| Key | Effect |
|---|---|
| `whatsapp` | Digits with country code (e.g. `8613800000000`): WhatsApp buttons in the header bar, footer, quote page and mobile contact bar |
| `contact_phone`, `address` | Footer, Organization schema and `llms.txt` |
| `form_endpoint` | Form service URL (e.g. Formspree `https://formspree.io/f/xxxx`): the quote form sends directly instead of opening an email draft; privacy notice updates automatically |
| `ga4_id` / `plausible_domain` | Analytics snippet; privacy notice updates automatically |
| `gsc_verification` | Google Search Console verification meta tag |
| `author` | Named author (`name`, `job_title`, `url`) for blog bylines and Person schema. Use a real, consenting person only |
| `social_profiles` | LinkedIn/YouTube/etc. URLs for Organization `sameAs` |
| `site_updated` | Default sitemap `lastmod` and CSS/JS cache-busting version; bump on each release |

Site content (products, applications, SEO fields, FAQs, case figures) lives in `site_data.py`; page templates in `build.py`. After adding or replacing a product image, run `python tools/optimize_images.py` (needs Pillow) to regenerate the WebP and 1200×630 social images, and commit the outputs. `build.py` and `marine_blog.py` generate HTML, sitemap, RSS and downloads. Blog articles live in `content/blog/`; see [BLOG_PUBLISHING.md](BLOG_PUBLISHING.md) for the publishing workflow and topic plan. Styles, JavaScript and images are retained in `dist/assets/`.

## Enquiries

The site displays the confirmed business email and prepares project briefs locally in the visitor's browser. **Open email draft** opens the visitor's mail application with the recipient and brief. The visitor must send that email. This version does not submit enquiries to a server, store leads in a database or claim that a draft has been delivered.

## Hosting

Hosting is managed by Sites using the existing identity in `.openai/hosting.json`; the static directory is `dist`. GitHub is a source mirror. A GitHub push alone does not publish a new Sites version. See [DEPLOYMENT.md](DEPLOYMENT.md) for DNS and publication steps. Keep credentials outside source files and commits.

## Product attribution

Equipment and manufacturer references are attributed to Boya Gongdao / ROBOOCEAN. Asset provenance is in `sources.json`. Manufacturer projects are not presented as projects delivered by PanPan Marine.

The site does not claim exclusive distribution, unverified CE certification, overseas repair centres or guaranteed turnaround times. Configurations, authorization scope, acceptance and commercial commitments are confirmed per project. `authorization_verified` stays false until the applicable documentation is verified.

Source differences remain explicit: R-30/R-45 images and figures may refer to different versions; AD-400 official-page range is 5 km while the brochure says 5.5 km; AD-100's 5 m3/h describes the paired separation system, not verified robot dredging productivity.
