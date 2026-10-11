# PanPan Marine

English B2B website for industrial underwater inspection and maintenance equipment.

- Brand: PanPan Marine, a PanPanTech brand
- Website operator: Guangzhou PanPanTech Co., Ltd.
- Primary domain: https://www.panpanmarine.com
- Enquiries: panda@panpantechnology.com
- Source repository: https://github.com/PanPanTech/panpanmarine.com

The site contains 31 content routes: four application pillars, five equipment models, manufacturer case studies, support, buying resources, company information, a project-brief form and legal pages, plus a blog hub, three topic pages and three initial buying guides.

## Build and preview

Python 3 standard library only; no package installation is required.

Run `python build.py`, then `python -m http.server 4173 --directory dist --bind 127.0.0.1`. In another terminal, run `python validate.py` and `node --check dist/assets/site.js`.

`config.json` controls the brand, operator, email and canonical origin. `build.py` and `marine_blog.py` generate HTML, sitemap, RSS and downloads. Blog articles live in `content/blog/`; see [BLOG_PUBLISHING.md](BLOG_PUBLISHING.md) for the publishing workflow and topic plan. Styles, JavaScript and images are retained in `dist/assets/`.

## Enquiries

The project-brief form sends enquiries to the shared PanPanTech enquiry service (Feishu + Zoho), tagged `lead_brand: "PanPan Marine"`. If online sending fails, the visitor can download the brief or open an email draft to the confirmed business email.

## Hosting

GitHub Pages, deployed automatically from `main` by `.github/workflows/pages.yml` (static directory `dist`). See [DEPLOYMENT.md](DEPLOYMENT.md) for DNS and publication steps. Keep credentials outside source files and commits.

## Product attribution

Equipment and manufacturer references are attributed to Boya Gongdao / ROBOOCEAN. Asset provenance is in `sources.json`. Manufacturer projects are not presented as projects delivered by PanPan Marine.

The site does not claim exclusive distribution, unverified CE certification, overseas repair centres or guaranteed turnaround times. Configurations, authorization scope, acceptance and commercial commitments are confirmed per project. `authorization_verified` stays false until the applicable documentation is verified.

Source differences remain explicit: R-30/R-45 images and figures may refer to different versions; AD-400 official-page range is 5 km while the brochure says 5.5 km; AD-100's 5 m3/h describes the paired separation system, not verified robot dredging productivity.
