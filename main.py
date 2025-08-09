import os
if not os.environ.get("CI_ALLOW_NON_INTEL"):
    check_platform()
def check_platform():
    system = platform.system()
    machine = platform.machine()
    mac_ver, _, _ = platform.mac_ver()

    if system != "Darwin":
        sys.exit("❌ Bu program yalnızca macOS üzerinde çalışır.")

    if not (machine.startswith("i") or machine.startswith("x86")):
        sys.exit("❌ Bu program yalnızca Intel tabanlı macOS cihazlarda çalışır (Apple Silicon desteklenmiyor).")

    try:
        major, minor, *_ = [int(x) for x in mac_ver.split(".")]
    except ValueError:
        sys.exit("❌ macOS sürümü algılanamadı.")

    if (major, minor) < (10, 14):
        sys.exit("❌ macOS Mojave (10.14) veya üzeri gereklidir.")

check_platform()

import argparse, csv
from pathlib import Path
from core import ela as ela_mod
from core import hash_utils
from core import exif_reader
from core import gps_checker
from core import face_detector
from core import gan_detector_resnet
from core import report as report_mod

def analyze_image(image_path: Path, watermark=None):
    image_path = Path(image_path)
    out_pdf = Path('output') / f'{image_path.stem}_report.pdf'

    # Hashes
    hashes = hash_utils.compute_hashes(image_path)

    # EXIF
    exif = exif_reader.read_exif(image_path)

    # GPS
    gps = gps_checker.gps_consistency(exif)

    # Faces
    faces = face_detector.detect_faces(image_path)

    # ELA
    ela = ela_mod.ela_analyze(image_path)

    # GAN
    model, model_note = gan_detector_resnet.load_model()
    gan = gan_detector_resnet.score_image(model, image_path)
    if model_note:
        gan['note'] = model_note

    results = {'hash': hashes, 'exif': exif, 'gps': gps, 'faces': faces, 'ela': ela, 'gan': gan}

    # PDF
    report_mod.render_report(out_pdf, image_path, results, ela_image_path=ela.get('ela_image_path'), watermark=watermark)

    return results, str(out_pdf)

def analyze_folder(folder_path: Path, watermark=None):
    folder_path = Path(folder_path)
    rows = []
    pdfs = []
    for img in sorted(folder_path.iterdir()):
        if img.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.tif', '.tiff', '.bmp'}:
            res, pdf = analyze_image(img, watermark=watermark)
            pdfs.append(pdf)
            rows.append({
                'file': img.name,
                'sha256': res['hash']['sha256'],
                'ahash': res['hash']['ahash'],
                'dhash': res['hash']['dhash'],
                'phash': res['hash']['phash'],
                'ela_score': res['ela']['ela_score'],
                'face_count': res['faces'].get('face_count', 0),
                'gan_score': res['gan'].get('gan_score'),
            })
    csv_path = Path('output') / 'summary.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ['file'])
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return str(csv_path), pdfs

def main():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--image', type=str, help='Tek görsel yolu')
    g.add_argument('--folder', type=str, help='Klasör yolu')
    parser.add_argument('--watermark', type=str, default=None, help='PDF watermark yazısı (opsiyonel)')
    args = parser.parse_args()

    if args.image:
        res, pdf = analyze_image(Path(args.image), watermark=args.watermark)
        print('PDF:', pdf)
    else:
        csv_path, pdfs = analyze_folder(Path(args.folder), watermark=args.watermark)
        print('CSV:', csv_path)
        print('PDF sayısı:', len(pdfs))

if __name__ == '__main__':
    main()
