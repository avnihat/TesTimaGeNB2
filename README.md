# TesTimaGeNB (Quick Wins Edition)

Bu sürüm aşağıdaki hızlı kazanımları uygular:
- Gerçek **ELA analizi** (Pillow) ve skor.
- **Hash paketleri**: sha256, aHash, dHash, pHash; QR üretimi ve `data/phash_db.json` eşlemesi.
- **Bağımlılıklar** güncellendi (TensorFlow opsiyonel).
- **Model yoksa zarif düşüş**: GAN tespiti modülü model yoksa otomatik pasif.
- **PDF raporu** tablo düzeni ve uzun alan yönetimi ile geliştirildi.
- **Klasör analizi**: toplu işleme + özet CSV; her görsel için PDF sayfası.

## Hızlı Başlangıç (CLI)
```bash
pip install -r requirements.txt
python main.py --image path/to/img.jpg  # Tek görsel
python main.py --folder path/to/images  # Klasör (CSV + PDF)
```

## GUI (basit)
```bash
python gui.py
```

> Not: `models/gan_detector_resnet.h5` dosyası yoksa GAN tespiti otomatik devre dışı kalır.
