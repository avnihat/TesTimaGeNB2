import sys
import platform
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

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QTextEdit, QHBoxLayout, QLineEdit
from PyQt5.QtCore import Qt
from core import gan_detector_resnet
from main import analyze_image, analyze_folder

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TesTimaGeNB – Quick Wins')
        self.resize(640, 480)
        layout = QVBoxLayout(self)

        self.info = QLabel('Bir görsel veya klasör seçin. Model dosyası yoksa GAN tespiti otomatik devre dışı.')
        layout.addWidget(self.info)

        row = QHBoxLayout()
        self.path_edit = QLineEdit()
        row.addWidget(self.path_edit)
        btn_img = QPushButton('Görsel Seç')
        btn_img.clicked.connect(self.pick_image)
        row.addWidget(btn_img)
        btn_dir = QPushButton('Klasör Seç')
        btn_dir.clicked.connect(self.pick_folder)
        row.addWidget(btn_dir)
        layout.addLayout(row)

        self.watermark = QLineEdit()
        self.watermark.setPlaceholderText('PDF watermark (opsiyonel)')
        layout.addWidget(self.watermark)

        self.run_btn = QPushButton('Analiz Et')
        self.run_btn.clicked.connect(self.run_analysis)
        layout.addWidget(self.run_btn)

        self.out = QTextEdit()
        self.out.setReadOnly(True)
        layout.addWidget(self.out)

        # Show GAN availability
        _, note = gan_detector_resnet.load_model()
        if note:
            self.info.setText(self.info.text() + f"\nDurum: {note}")

    def pick_image(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Görsel seç', '', 'Images (*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp)')
        if path:
            self.path_edit.setText(path)

    def pick_folder(self):
        path = QFileDialog.getExistingDirectory(self, 'Klasör seç')
        if path:
            self.path_edit.setText(path)

    def run_analysis(self):
        p = self.path_edit.text().strip()
        if not p:
            self.out.setPlainText('Lütfen bir yol seçin.')
            return
        wm = self.watermark.text().strip() or None
        path = Path(p)
        try:
            if path.is_dir():
                csv_path, pdfs = analyze_folder(path, watermark=wm)
                self.out.setPlainText(f'Klasör işlemi tamamlandı.\nCSV: {csv_path}\nPDF sayısı: {len(pdfs)}')
            else:
                res, pdf = analyze_image(path, watermark=wm)
                lines = ['Tek görsel analizi tamamlandı:', f'PDF: {pdf}', f'ELA: {res["ela"]["ela_score"]}', f'Face: {res["faces"].get("face_count")}']
                self.out.setPlainText('\n'.join(lines))
        except Exception as e:
            self.out.setPlainText(f'Hata: {e}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec_())
