"""Build one gallery row per product folder, with browser-friendly images."""
from html import escape
from pathlib import Path
import re
import shutil

from PIL import Image, ImageOps
from pillow_heif import register_heif_opener

register_heif_opener()
ROOT = Path(__file__).resolve().parents[1]
FORMATS = {'.jpg', '.jpeg', '.png', '.webp', '.heic', '.heif'}


def label(path):
    return re.sub(r'^\d+[ _-]+', '', path.stem).replace('_', ' ')


def convert(source, destination):
    with Image.open(source) as original:
        photo = ImageOps.exif_transpose(original).convert('RGB')
        photo.thumbnail((1600, 1600))
        # Recreate pixels to omit EXIF, including location, from public images.
        clean = Image.new('RGB', photo.size)
        clean.paste(photo)
        clean.save(destination, quality=85, optimize=True)
        return photo.size


def build(source=ROOT / 'billeder', output=ROOT / 'dist'):
    output.mkdir(parents=True, exist_ok=True)
    assets = output / 'billeder'
    assets.mkdir(exist_ok=True)
    used = {'profil.jpg'}
    convert(source / 'profilbillede.png', assets / 'profil.jpg')
    rows = []
    for folder in sorted(source.iterdir()):
        if not folder.is_dir() or folder.name.startswith('.'):
            continue
        photos = sorted(p for p in folder.iterdir() if p.is_file() and not p.name.startswith('.') and p.suffix.lower() in FORMATS)
        if not photos:
            continue
        title = escape(label(folder))
        cards = []
        for number, photo in enumerate(photos, 1):
            filename = f'{len(rows)+1}-{number}.jpg'
            used.add(filename)
            width, height = convert(photo, assets / filename)
            caption = escape(label(photo))
            # shortcut: Garn er kun et udkast på første billede; erstat med rigtige oplysninger senere.
            yarn = '<ul class="yarn"><li>Garn 1</li><li>Garn 2</li><li>Garn 3</li></ul>' if not rows and number == 1 else ''
            cards.append(f'<figure><a class="photo" href="billeder/{filename}" aria-label="Se {title}: {caption} i stort format"><img src="billeder/{filename}" width="{width}" height="{height}" alt="{title} — {caption}" loading="lazy"></a><figcaption>{caption}{yarn}</figcaption></figure>')
        count = f'{len(photos)} variant' + ('er' if len(photos) != 1 else '')
        rows.append(f'<section class="product" aria-labelledby="produkt-{len(rows)}"><div class="product-heading"><div><span class="number">{len(rows)+1:02d}</span><h2 id="produkt-{len(rows)}">{title}</h2></div><span class="count">{count}</span></div><div class="photos" tabindex="0" role="region" aria-label="{title} — rul sidelæns for flere billeder">{"".join(cards)}</div></section>')
    template = (ROOT / 'index.html').read_text()
    (output / 'index.html').write_text(template.replace('<!-- GALLERY -->', '\n'.join(rows) or '<p>Der er snart strik at se her.</p>'))
    for name in ('style.css', 'gallery.js'):
        shutil.copyfile(ROOT / name, output / name)
    for old in assets.glob('*.jpg'):
        if old.name not in used:
            old.unlink()
    print(f'Bygget {len(rows)} produktrækker i {output}')


if __name__ == '__main__':
    build()
