# PanPan Marine deployment

Primary domain: `panpanmarine.com`. Hosting uses Sites; preserve `.openai/hosting.json`. The GitHub repository is a source mirror, not the hosting provider.

## Alibaba Cloud DNS

These records were returned by Sites for the apex domain on 9 October 2026. Add them in the existing `panpanmarine.com` DNS zone, with the default routing line and a normal TTL such as 600 seconds. Verification TXT records are public DNS values, not API credentials.

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 162.159.143.30 |
| A | @ | 172.66.3.26 |
| TXT | _openai-site-verification | openai-site-verification=VvrvcF83mxBfKnppPoWEDjGz4NQzLFgMh0nIf0zpVTs |
| TXT | _cf-custom-hostname | 8156c8ce-9f33-4d02-b908-48a869befefd |

Retain unrelated mail and verification records. If the apex has a parking CNAME or conflicting web A/AAAA records, review and replace only those conflicting website records. Do not change nameservers or unrelated records.

After propagation, refresh the custom-domain status in Sites. Confirm hostname and SSL are active, then verify the homepage, equipment routes, enquiry page and sitemap over HTTPS.

`www.panpanmarine.com` needs a separate hostname binding and its returned validation records before use; it is not configured by this file.

## Updates

Run `python build.py`; run the local HTTP server and `python validate.py`. Synchronize the exact source through the Sites workflow, save its matching archive, and deploy that saved version. Mirror the source to GitHub. A GitHub push alone does not deploy Sites.

Enquiries use `panda@panpantechnology.com`. The brief form runs locally and opens a mail draft; visitors send it through their own mail application. It does not claim server-side delivery.

These instructions do not by themselves confirm DNS or HTTPS activation. Verify returned hosting and domain states after applying the configuration.
