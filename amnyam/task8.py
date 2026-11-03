import sys
import numpy as np
import soundfile as sf
import sounddevice as sd
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QFileDialog,
                             QSlider, QLabel, QVBoxLayout)
from PyQt5.QtCore import Qt


class AudioPanApp(QWidget):
    def __init__(self):
        super().__init__()
        self.data = None
        self.sr = None
        self.setWindowTitle("Аудіо: канали, гучність, панорама")
        self.layout = QVBoxLayout()

        self.btn_load = QPushButton("Обрати аудіофайл")
        self.btn_load.clicked.connect(self.load_file)

        self.btn_left = QPushButton("Тільки лівий канал")
        self.btn_left.clicked.connect(lambda: self.play(channel='left'))

        self.btn_right = QPushButton("Тільки правий канал")
        self.btn_right.clicked.connect(lambda: self.play(channel='right'))

        self.btn_both = QPushButton("Обидва канали")
        self.btn_both.clicked.connect(lambda: self.play(channel='both'))

        self.lbl_vol = QLabel("Гучність: 100%")
        self.slider_vol = QSlider(Qt.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(100)
        self.slider_vol.valueChanged.connect(lambda v: self.lbl_vol.setText(f"Гучність: {v}%"))

        self.lbl_pan = QLabel("Панорама (L←→R): 0")
        self.slider_pan = QSlider(Qt.Horizontal)
        self.slider_pan.setRange(-100, 100)
        self.slider_pan.setValue(0)
        self.slider_pan.valueChanged.connect(lambda v: self.lbl_pan.setText(f"Панорама (L←→R): {v}"))

        for w in [self.btn_load, self.btn_left, self.btn_right, self.btn_both,
                  self.lbl_vol, self.slider_vol, self.lbl_pan, self.slider_pan]:
            self.layout.addWidget(w)

        self.setLayout(self.layout)

    def load_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Аудіофайл", "", "Audio (*.wav *.flac *.ogg)")
        if path:
            self.data, self.sr = sf.read(path, always_2d=True)

    def play(self, channel='both'):
        if self.data is None:
            return
        d = self.data.copy()

        if channel == 'left':
            d[:, 1] = 0
        elif channel == 'right':
            d[:, 0] = 0

        vol = self.slider_vol.value() / 100.0
        pan = self.slider_pan.value() / 100.0

        d[:, 0] *= (1 - max(0, pan))
        d[:, 1] *= (1 + min(0, pan))
        d *= vol

        sd.play(d, self.sr)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = AudioPanApp()
    w.show()
    sys.exit(app.exec_())