from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from pathlib import Path
import textwrap

def _kv_block(c, x, y, key, value, width, leading=12):
    key = str(key)
    value = '' if value is None else str(value)
    max_chars = int(width / 6)
    lines = textwrap.wrap(value, max_chars) or ['']
    c.setFont('Helvetica-Bold', 10)
    c.drawString(x, y, key + ':')
    c.setFont('Helvetica', 10)
    yy = y - leading
    for line in lines:
        c.drawString(x + 90, yy, line)
        yy -= leading
    return yy - leading

def render_report(pdf_path, image_path, results: dict, ela_image_path=None, watermark=None):
    pdf_path = Path(pdf_path)
    pdf_path.parent.mkdir(parents=True, exist_ok=True)

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    W, H = A4
    margin = 2*cm
    x = margin
    y = H - margin

    c.setFont('Helvetica-Bold', 16)
    c.drawString(x, y, 'Görsel Analiz Raporu')
    if watermark:
        c.setFont('Helvetica', 24)
        c.setFillGray(0.9)
        c.drawString(W/2-80, H/2, watermark)
        c.setFillGray(0)

    y -= 30
    try:
        img = ImageReader(str(image_path))
        c.drawImage(img, x, y-150, width=120, height=120, preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    y -= 20
    c.setFont('Helvetica-Bold', 12)
    c.drawString(x+140, y, 'Özet Sonuçlar')
    y -= 10

    keys = [
        ('AI/GAN Skoru', results.get('gan', {}).get('gan_score')),
        ('ELA Skoru', results.get('ela', {}).get('ela_score')),
        ('Yüz Sayısı', results.get('faces', {}).get('face_count')),
        ('EXIF Yazılım', results.get('exif', {}).get('Software')),
        ('GPS Uyarı', ', '.join(results.get('gps', {}).get('gps_uyari') or []) if results.get('gps', {}).get('gps_uyari') else '—'),
    ]
    yy = y
    for k, v in keys:
        yy = _kv_block(c, x+140, yy, k, v, width=300)

    c.setFont('Helvetica-Bold', 12)
    c.drawString(x, yy, 'İmzalar')
    yy -= 10
    for k in ['sha256', 'ahash', 'dhash', 'phash']:
        val = results.get('hash', {}).get(k)
        yy = _kv_block(c, x, yy, k.upper(), val, width=450)

    qr = results.get('hash', {}).get('qr_code')
    if qr:
        try:
            c.drawImage(ImageReader(qr), W - margin - 120, margin, width=120, height=120, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

    if ela_image_path:
        try:
            c.drawImage(ImageReader(ela_image_path), x, margin, width=200, height=200, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass

    c.showPage()
    c.save()
