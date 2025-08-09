import hashlib, json
from pathlib import Path
from PIL import Image
import imagehash
import qrcode

DB_PATH = Path('data/phash_db.json')

def ensure_dirs():
    Path('output').mkdir(parents=True, exist_ok=True)
    Path('data').mkdir(parents=True, exist_ok=True)

def compute_hashes(image_path):
    ensure_dirs()
    image_path = Path(image_path)
    # sha256
    h = hashlib.sha256()
    with open(image_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    sha256 = h.hexdigest()

    with Image.open(image_path) as im:
        ah = str(imagehash.average_hash(im))
        dh = str(imagehash.dhash(im))
        ph = str(imagehash.phash(im))

    qr_path = Path('output') / (image_path.stem + '_qr.png')
    img = qrcode.make(sha256)
    img.save(qr_path)

    match = phash_db_match(ph)
    return {
        'sha256': sha256,
        'ahash': ah,
        'dhash': dh,
        'phash': ph,
        'qr_code': str(qr_path),
        'veri_tabani_eslesme': match,
    }

def phash_db_match(phash_value, max_distance=5):
    ensure_dirs()
    if not DB_PATH.exists():
        DB_PATH.write_text(json.dumps({'known': []}, ensure_ascii=False, indent=2), encoding='utf-8')
    data = json.loads(DB_PATH.read_text(encoding='utf-8'))
    known = data.get('known', [])
    # simple Hamming distance on hex strings via imagehash
    try:
        target = imagehash.hex_to_hash(phash_value)
    except Exception:
        return None
    best = None
    for item in known:
        try:
            h = imagehash.hex_to_hash(item.get('phash', ''))
            dist = target - h
            if best is None or dist < best['distance']:
                best = {'distance': int(dist), 'meta': item.get('meta')}
        except Exception:
            continue
    if best and best['distance'] <= max_distance:
        return best
    return None
