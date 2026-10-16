"""Static editorial publishing: content/blog/*.json -> pages and RSS."""
from datetime import date, datetime, timezone
from email.utils import format_datetime
from html import escape, unescape
from math import ceil
from pathlib import Path
import json
import os
import re

CATEGORIES = {
    'equipment-selection': ('Equipment selection', 'Compare inspection tasks, sensing, payloads and the complete field system before requesting a quotation.'),
    'tunnel-inspection': ('Tunnel inspection', 'Plan flooded-tunnel procurement around route geometry, usable inspection evidence and a reviewed recovery approach.'),
    'cleaning-dredging': ('Cleaning & dredging', 'Identify whether your task involves surface deposits or loose sediment, then specify the tools and supporting system.'),
    'offshore-subsea': ('Offshore & subsea', 'Plan offshore wind, cable and subsea structure work around the deliverable, the ROV class and the launch and recovery arrangement.'),
    'surface-water': ('Surface vessels & survey', 'Specify unmanned surface vessels for floating-debris collection and bathymetric survey, including shore facilities and local approvals.'),
}


def active_categories(posts):
    """Only categories with at least one published post get a topic page and a navigation tab."""
    used = {p['category_slug'] for p in posts}
    return {slug: value for slug, value in CATEGORIES.items() if slug in used}


# Never send visitors to the manufacturer's own websites.
BLOCKED_LINK_DOMAINS = ('boyagongdao.com', 'roboocean.com', 'robosea')


def build_date():
    """Publication cut-off. BLOG_BUILD_DATE=YYYY-MM-DD previews scheduled posts locally."""
    override = os.environ.get('BLOG_BUILD_DATE')
    return date.fromisoformat(override) if override else date.today()


def article_path(post):
    return '/blog/' + post['slug'] + '/'


def plain_text(value):
    return re.sub(r'\s+', ' ', unescape(re.sub(r'<[^>]+>', ' ', value))).strip()


def load_posts(root):
    posts = []
    for filename in sorted((root / 'content' / 'blog').glob('*.json')):
        if filename.name.startswith('_'):
            continue
        post = json.loads(filename.read_text(encoding='utf-8-sig'))
        if post.get('status', 'draft') != 'published':
            continue
        if date.fromisoformat(post['published_at']) > build_date():
            continue  # scheduled: published by the daily rebuild on that date
        required = ('slug', 'title', 'description', 'category_slug', 'answer', 'image', 'alt', 'sections', 'faq', 'sources', 'published_at', 'updated_at')
        for key in required:
            if not post.get(key):
                raise ValueError(f'{filename.name}: missing {key}')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', post['slug']):
            raise ValueError(f'{filename.name}: invalid slug')
        if post['category_slug'] not in CATEGORIES:
            raise ValueError(f'{filename.name}: unknown category')
        published, updated = date.fromisoformat(post['published_at']), date.fromisoformat(post['updated_at'])
        if updated < published:
            raise ValueError(f'{filename.name}: update precedes publication')
        if not (root / 'dist' / 'assets' / post['image']).is_file():
            raise ValueError(f'{filename.name}: missing image')
        ids = [s['id'] for s in post['sections']]
        if len(ids) != len(set(ids)) or any(not re.fullmatch(r'[a-z0-9-]+', i) for i in ids):
            raise ValueError(f'{filename.name}: invalid section IDs')
        post['category'] = CATEGORIES[post['category_slug']][0]
        text = post['answer'] + ' ' + ' '.join(s['title'] + ' ' + plain_text(s['html']) for s in post['sections']) + ' ' + ' '.join(f['question'] + ' ' + f['answer'] for f in post['faq'])
        post['word_count'] = len(re.findall(r"[A-Za-z][A-Za-z0-9'-]*", text))
        post['read_minutes'] = max(1, ceil(post['word_count'] / 200))
        posts.append(post)
    if len({p['slug'] for p in posts}) != len(posts):
        raise ValueError('Duplicate article slug')
    # Links to posts that are not published yet render as plain text until their date.
    live = {p['slug'] for p in posts}
    def keep_live(match):
        return match.group(0) if match.group(1) in live else match.group(2)
    for p in posts:
        for section in p['sections']:
            section['html'] = re.sub(r'<a href="/blog/([a-z0-9-]+)/">(.*?)</a>', keep_live, section['html'])
    return sorted(posts, key=lambda p: (p['published_at'], p['slug']), reverse=True)


def pretty_date(value):
    d = date.fromisoformat(value)
    return f'{d.day} {d.strftime("%B %Y")}'


def card(post):
    url = article_path(post)
    return f'''<article class="blog-card"><a class="blog-card-image" href="{url}"><img src="/assets/{escape(post['image'], quote=True)}" alt="{escape(post['alt'], quote=True)}" width="900" height="650" loading="lazy"></a><div class="blog-card-copy"><a class="eyebrow" href="/blog/topics/{post['category_slug']}/">{escape(post['category'])}</a><h3><a href="{url}">{escape(post['title'])}</a></h3><p>{escape(post['description'])}</p><p class="meta"><time datetime="{post['published_at']}">{pretty_date(post['published_at'])}</time> · {post['read_minutes']} min read</p><a class="text-link" href="{url}">Read the guide</a></div></article>'''


def cards(posts):
    return '<div class="blog-grid">' + ''.join(card(p) for p in posts) + '</div>'


def latest_section(posts):
    if not posts:
        return ''
    return '<section class="section band"><div class="wrap"><div class="section-heading"><div><p class="eyebrow">THE PANPAN MARINE BLOG</p><h2>Prepare a better purchase.</h2></div><a class="text-link" href="/blog/">Explore all buying guides</a></div>' + cards(posts[:3]) + '</div></section>'


def related_guide(posts, category):
    matches = [p for p in posts if p['category_slug'] == category]
    if not matches:
        return ''
    p = matches[0]
    return f'<section class="wrap section blog-related-note"><p class="eyebrow">DEEPER PROCUREMENT GUIDANCE</p><h2>{escape(p["title"])}</h2><p>{escape(p["description"])}</p><a class="text-link" href="{article_path(p)}">Read the buying guide</a></section>'


def topic_nav(active='', categories=None):
    links = [('','All guides')] + [(slug, name) for slug, (name, _) in (categories or CATEGORIES).items()]
    return '<nav class="blog-topics" aria-label="Blog topics">' + ''.join(f'<a href="/blog/{"topics/" + slug + "/" if slug else ""}" {"aria-current=\"page\"" if active == slug else ""}>{escape(name)}</a>' for slug, name in links) + '</nav>'


def breadcrumbs(origin, parts):
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [dict({'@type': 'ListItem'}, position=i, name=name, item=origin + path) for i, (name, path) in enumerate(parts, 1)]}


def render_blog(root, posts, write, intro, cta, origin, company, brand):
    cats = active_categories(posts)
    body = intro('BLOG / BUYING GUIDES', 'Better briefs.<br>Better equipment decisions.', 'Practical guidance for teams buying underwater inspection, cleaning and dredging equipment.')
    body += '<section class="wrap section"><div class="blog-index-heading"><p>Start with your task, then review the configuration, evidence and responsibilities behind the quotation.</p><a class="text-link" href="/blog/feed.xml">Follow the RSS feed</a></div>' + topic_nav('', cats) + cards(posts) + '</section>'
    body += '<section class="wrap section two-col"><div><p class="eyebrow">TECHNICAL RESOURCES</p><h2>Keep the working documents close.</h2><p>Use the sensing guide and downloadable project checklist alongside these buying guides.</p><a class="text-link" href="/resources/">Open technical resources</a></div><div><p class="eyebrow">OUR EDITORIAL APPROACH</p><h2>Source, scope and configuration.</h2><p>Guides distinguish manufacturer information from project-planning recommendations. Figures and product suitability are checked against the supplied version and proposed application.</p><a class="text-link" href="/about/">About PanPan Marine</a></div></section>' + cta()
    collection = {'@context': 'https://schema.org', '@type': 'CollectionPage', 'name': 'PanPan Marine Blog', 'url': origin + '/blog/', 'mainEntity': {'@type': 'ItemList', 'itemListElement': [dict({'@type': 'ListItem'}, position=i, url=origin + article_path(p), name=p['title']) for i, p in enumerate(posts, 1)]}}
    lastmod = max((p['updated_at'] for p in posts), default=None)
    write('/blog/', 'Underwater Robotics Blog & Buying Guides', 'Buying guides for industrial inspection ROVs, flooded tunnel inspection, underwater cleaning and dredging systems.', body, schema_extra=[collection, breadcrumbs(origin, [('Home','/'), ('Blog','/blog/')])], lastmod=lastmod)
    for slug, (name, description) in cats.items():
        selected = [p for p in posts if p['category_slug'] == slug]
        body = intro('BLOG / ' + name.upper(), name + ' guides', description)
        body += '<section class="wrap section">' + topic_nav(slug, cats) + cards(selected) + '</section>' + cta()
        # A useful navigation page; index once the topic has a substantial collection.
        write('/blog/topics/' + slug + '/', name + ' Buying Guides', description, body, noindex=len(selected) < 3, lastmod=max((p['updated_at'] for p in selected), default=None))
    for p in posts:
        path = article_path(p)
        title, description = p['title'], p['description']
        meta = f'<p class="blog-meta">By PanPan Marine · <time datetime="{p["published_at"]}">Published {pretty_date(p["published_at"])}</time>'
        if p['updated_at'] != p['published_at']:
            meta += f' · Updated <time datetime="{p["updated_at"]}">{pretty_date(p["updated_at"])}</time>'
        meta += f' · {p["read_minutes"]} min read</p>'
        body = intro('BLOG / ' + p['category'].upper(), escape(title), escape(description))
        body += '<div class="wrap breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / ' + escape(p['category']) + '</div>'
        toc = ''.join(f'<a href="#{s["id"]}">{escape(s["title"])}</a>' for s in p['sections']) + '<a href="#faq">Frequently asked questions</a><a href="#sources">Sources &amp; scope</a>'
        body += '<article class="wrap section blog-layout"><aside class="blog-aside"><nav aria-label="On this page"><h2>On this page</h2>' + toc + '</nav><div class="blog-aside-cta"><h3>Put your brief to work.</h3><p>Share your task and site conditions for a configuration review.</p><a class="button" href="/request-a-proposal/">Plan your project</a></div></aside><div class="blog-content">' + meta
        body += '<section class="blog-answer" aria-labelledby="quick-answer"><h2 id="quick-answer">The short answer</h2><p>' + escape(p['answer']) + '</p></section>'
        body += f'<figure class="blog-figure"><img src="/assets/{escape(p["image"], quote=True)}" alt="{escape(p["alt"], quote=True)}" width="900" height="650"><figcaption>Manufacturer equipment illustration. Configuration and appearance depend on the supplied version.</figcaption></figure>'
        for s in p['sections']:
            html = s['html'] if 'class="table-scroll"' in s['html'] else re.sub(r'(<table\b.*?</table>)', r'<div class="table-scroll">\1</div>', s['html'], flags=re.S | re.I)
            body += f'<section id="{s["id"]}"><h2>{escape(s["title"])}</h2>{html}</section>'
        body += '<section id="faq"><h2>Frequently asked questions</h2><div class="faq">' + ''.join(f'<details><summary>{escape(f["question"])}</summary><p>{escape(f["answer"])}</p></details>' for f in p['faq']) + '</div></section>'
        sources = ''.join('<li>' + (f'<a href="{escape(s["url"], quote=True)}" rel="noopener">{escape(s["title"])}</a>' if s.get('url') and not any(d in s['url'] for d in BLOCKED_LINK_DOMAINS) else escape(s['title'])) + (f' — {escape(s["note"])}' if s.get('note') else '') + '</li>' for s in p['sources'])
        body += '<section class="blog-source-note" id="sources"><h2>Sources &amp; scope</h2><ul>' + sources + '</ul><p>This guide offers procurement-planning guidance. Manufacturer specifications, site feasibility and contractual responsibilities are confirmed for the proposed system; this page is not an operating procedure.</p></section></div></article>'
        other = [a for a in posts if a['slug'] != p['slug']][:2]
        body += '<section class="section band"><div class="wrap"><p class="eyebrow">CONTINUE YOUR RESEARCH</p><h2>Related buying guides.</h2>' + cards(other) + '</div></section>' + cta()
        schema = {'@context': 'https://schema.org', '@type': 'BlogPosting', '@id': origin + path + '#article', 'headline': title, 'description': description, 'url': origin + path, 'mainEntityOfPage': origin + path, 'datePublished': p['published_at'], 'dateModified': p['updated_at'], 'inLanguage': 'en', 'articleSection': p['category'], 'wordCount': p['word_count'], 'image': origin + '/assets/' + p['image'], 'author': {'@type':'Organization','name':brand,'url':origin + '/about/'}, 'publisher': {'@type':'Organization','name':company,'url':origin}, 'citation': [s['url'] for s in p['sources'] if s.get('url')]}
        fq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [{'@type':'Question','name':f['question'],'acceptedAnswer':{'@type':'Answer','text':f['answer']}} for f in p['faq']]}
        write(path, title, description, body, schema_extra=[schema, fq, breadcrumbs(origin, [('Home','/'), ('Blog','/blog/'), (title,path)])], og_type='article', og_image=p['image'], lastmod=p['updated_at'])
    feed = '<?xml version="1.0" encoding="UTF-8"?><rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>PanPan Marine Blog</title><link>' + escape(origin + '/blog/') + '</link><description>Underwater robotics buying guides and procurement planning.</description><language>en</language><atom:link href="' + escape(origin + '/blog/feed.xml', quote=True) + '" rel="self" type="application/rss+xml"/>'
    for p in posts:
        url = origin + article_path(p)
        pub = format_datetime(datetime.combine(date.fromisoformat(p['published_at']), datetime.min.time(), timezone.utc), usegmt=True)
        feed += '<item><title>' + escape(p['title']) + '</title><link>' + escape(url) + '</link><guid isPermaLink="true">' + escape(url) + '</guid><description>' + escape(p['description']) + '</description><category>' + escape(p['category']) + '</category><pubDate>' + pub + '</pubDate></item>'
    (root / 'dist' / 'blog' / 'feed.xml').write_text(feed + '</channel></rss>', encoding='utf-8')
