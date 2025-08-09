# TesTimaGeNB (Quick Wins + macOS Intel Mojave+)

- macOS **Intel** ve **10.14 Mojave+** koşulu zorunlu (CI ortamında bypass).
- ELA analizi, hash paketleri, EXIF/GPS kontrolü, yüz tespiti, PDF rapor.
- Klasör analizi için CSV + sayfa başına PDF.
- TensorFlow opsiyonel; model yoksa GAN tespiti pasif.

## Çalıştırma
```bash
pip install -r requirements.txt
python main.py --image path/to/img.jpg
python main.py --folder path/to/dir
python gui.py
```

## GitHub Actions
`.github/workflows/build.yml` macOS-14 runner’da bağımlılıkları kurar, smoke test yapar ve zip artifact üretir.
CI içinde Intel/Mojave kontrolü `CI_ALLOW_NON_INTEL=1` ile devre dışı bırakılır.
