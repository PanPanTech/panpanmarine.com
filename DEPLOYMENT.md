# PanPan Marine deployment

Primary canonical domain: `www.panpanmarine.com`. Both apex and www are bound to the same site. Hosting uses Sites; preserve `.openai/hosting.json`. The GitHub repository is a source mirror, not the hosting provider.

## Alibaba Cloud DNS

These current records were returned by Sites and configured for apex/www on 9–10 October 2026. Add them in the existing `panpanmarine.com` DNS zone, with the default routing line and a normal TTL such as 600 seconds. Verification TXT records are public DNS values, not API credentials.

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 162.159.143.30 |
| A | @ | 172.66.3.26 |
| TXT | _openai-site-verification | openai-site-verification=VvrvcF83mxBfKnppPoWEDjGz4NQzLFgMh0nIf0zpVTs |
| CNAME | www | custom-domains.chatgpt.site |
| TXT | _openai-site-verification.www | openai-site-verification=Fwt7ea_ewb4PsZ-PKblG3FTm_xptj2O1v4ALkPpAusk |

Retain unrelated mail and verification records. If the apex has a parking CNAME or conflicting web A/AAAA records, review and replace only those conflicting website records. Do not change nameservers or unrelated records.

After propagation, refresh the custom-domain status in Sites. Confirm hostname and SSL are active, then verify the homepage, equipment routes, enquiry page and sitemap over HTTPS.

Both hostname bindings and SSL were confirmed active on 10 October 2026. Canonical tags use www; this does not configure an apex-to-www HTTP redirect.

## Updates

Run `python build.py`; run the local HTTP server and `python validate.py`. Synchronize the exact source through the Sites workflow, save its matching archive, and deploy that saved version. Mirror the source to GitHub. A GitHub push alone does not deploy Sites.

Enquiries use `panda@panpantechnology.com`. The brief form runs locally and opens a mail draft; visitors send it through their own mail application. It does not claim server-side delivery.

These instructions do not by themselves confirm DNS or HTTPS activation. Verify returned hosting and domain states after applying the configuration.
