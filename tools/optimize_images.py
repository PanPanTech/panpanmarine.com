"""One-off image optimisation (requires Pillow). Outputs are committed, so build.py stays stdlib-only.

Run after adding or replacing a source image in dist/assets/:  python tools/optimize_images.py
Produces <name>-600.webp, <name>-1200.webp and og-<name>.jpg (1200x630 social card).
"""
from pathlib import Path
from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / 'dist' / 'assets'
SOURCES = ['r-30.png', 'r-45.png', 'ad-400.jpg', 'a-80.jpg', 'ad-100.jpg']


def flatten(im):
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, 'white')
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert('RGB')


for name in SOURCES:
    src = ASSETS / name
    stem = src.stem
    im = Image.open(src)
    keep_alpha = im.mode in ('RGBA', 'LA', 'P')
    base = im.convert('RGBA') if keep_alpha else im.convert('RGB')
    for width in (600, 1200):
        w = min(width, base.width)
        out = base.resize((w, round(base.height * w / base.width)), Image.LANCZOS)
        out.save(ASSETS / f'{stem}-{width}.webp', 'WEBP', quality=80, method=6)
    flat = flatten(im)
    card = Image.new('RGB', (1200, 630), 'white')
    scale = min(1100 / flat.width, 560 / flat.height)
    fitted = flat.resize((round(flat.width * scale), round(flat.height * scale)), Image.LANCZOS)
    card.paste(fitted, ((1200 - fitted.width) // 2, (630 - fitted.height) // 2))
    card.save(ASSETS / f'og-{stem}.jpg', 'JPEG', quality=82, optimize=True, progressive=True)
    print(name, '->', [f'{stem}-600.webp', f'{stem}-1200.webp', f'og-{stem}.jpg'])
