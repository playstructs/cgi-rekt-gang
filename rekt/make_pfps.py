"""Makes the profile pictures this site hosts (rekt/pfp/) from the Rekt Gang
NFT archive (../RektGang, see its README.txt).

Every image becomes a 256px square WebP, rekt/pfp/<collection>/<id>.webp, and
rekt/pfp/collections.json lists each collection, its ids and any it lacks; the
gallery (rekt/runtime/gallery.js) reads it. The illustrated collections
(Wolves, Trippy Wolves, Bulls) are resized and compressed; the Chickens are
pixel art drawn 8x, so they keep every pixel (4x, lossless).

    ../RektGang/.venv/bin/python -I rekt/make_pfps.py [../RektGang]

Existing pictures are kept; delete one (or a collection's folder) to remake it.
"""
import json
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from PIL import Image

SIZE = 256
HERE = Path(__file__).resolve().parent
OUT = HERE / 'pfp'

# slug, name, tab label, pixel art, [(archive folder, first id, last id)]
COLLECTIONS = [
    ('wolves', 'Rekt Wolves', 'Wolves', False, [('Rekt Wolves', 1, 2222)]),
    ('trippy-wolves', 'Trippy Wolves', 'Trippy', False, [('Rekt Trippy Wolves', 1, 2222)]),
    ('bulls', 'Rekt Bulls', 'Bulls', False, [('Rekt Bulls', 1, 2269)]),
    ('chickens', 'Rekt Chickens', 'Chickens', True, [
        ('Rekt Chickens/Stargaze', 1, 5000),
        ('Rekt Chickens/Solana', 5001, 10000),
        ('Rekt Chickens/Polygon', 10001, 16420),
    ]),
    ('based-chickens', 'Based Rekt Chickens', 'Based', True, [('Rekt Chickens/Base', 1, 1000)]),
]


def source(folder, id_):
    for ext in ('png', 'webp', 'jpg', 'gif'):
        file = folder / 'images' / f'{id_}.{ext}'
        if file.exists():
            return file
    return None


def convert(job):
    src, dst, pixel = job
    if dst.exists():
        return
    with Image.open(src) as im:
        im.seek(0)
        if pixel:
            im = im.convert('RGBA').resize((SIZE, SIZE), Image.NEAREST)
            options = {'lossless': True, 'method': 6}
        else:
            im = im.convert('RGB').resize((SIZE, SIZE), Image.LANCZOS)
            options = {'quality': 80, 'method': 6}
        tmp = dst.with_suffix('.tmp')
        im.save(tmp, 'WEBP', **options)
        os.replace(tmp, dst)


def main(archive):
    jobs, manifest = [], []
    for slug, name, label, pixel, ranges in COLLECTIONS:
        (OUT / slug).mkdir(parents=True, exist_ok=True)
        missing = []
        for folder, first, last in ranges:
            for id_ in range(first, last + 1):
                src = source(archive / folder, id_)
                if src is None:
                    missing.append(id_)
                else:
                    jobs.append((src, OUT / slug / f'{id_}.webp', pixel))
        manifest.append({
            'slug': slug, 'name': name, 'label': label, 'pixel': pixel,
            'first': ranges[0][1], 'last': ranges[-1][2], 'missing': missing,
        })
        print(f'{slug}: {ranges[0][1]}-{ranges[-1][2]}, missing {missing or "none"}', flush=True)

    with ProcessPoolExecutor() as pool:
        for i, _ in enumerate(pool.map(convert, jobs, chunksize=32), 1):
            if i % 1000 == 0:
                print(f'{i}/{len(jobs)}', flush=True)

    (OUT / 'collections.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'{len(jobs)} pictures in {OUT}')


if __name__ == '__main__':
    main(Path(sys.argv[1] if len(sys.argv) > 1 else HERE.parent.parent / 'RektGang').resolve())
