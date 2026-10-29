import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QLineEdit, QSpinBox, QSlider, QGridLayout, QApplication
from model import Model

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("окно")
        self.resize(700, 300)

        self.model = Model()
        self.update_count = 0

        self.build_ui()
        self.model.attach(self.update_from_model)

    def build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        grid = QGridLayout()
        central.setLayout(grid)

        grid.addWidget(self.make_caption("A"), 0, 0)
        grid.addWidget(self.make_caption("<="), 0, 1)
        grid.addWidget(self.make_caption("B"), 0, 2)
        grid.addWidget(self.make_caption("<="), 0, 3)
        grid.addWidget(self.make_caption("C"), 0, 4)

        self.lines = []
        self.spins = []
        self.sliders = []

        for i in range(3):
            line = QLineEdit()
            spin = QSpinBox()
            slider = QSlider(Qt.Horizontal)

            spin.setRange(self.model.get_min(), self.model.get_max())
            slider.setRange(self.model.get_min(), self.model.get_max())

            line.editingFinished.connect(lambda idx=i: self.on_line(idx))
            spin.valueChanged.connect(lambda v, idx=i: self.on_spin_changed(idx, v))
            slider.valueChanged.connect(lambda v, idx=i: self.on_slider_changed(idx, v))

            grid.addWidget(line, 1, i * 2)
            grid.addWidget(spin, 2, i * 2)
            grid.addWidget(slider, 3, i * 2)

            self.lines.append(line)
            self.spins.append(spin)
            self.sliders.append(slider)

    def make_caption(self, text):
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        font = label.font()
        font.setPointSize(20)
        label.setFont(font)
        return label

    def on_line(self, index):
        text = self.lines[index].text().strip()
        try:
            value = int(text)
        except Exception:
            value = self.model.get_values()[index]
        self.model.set_value(index, value)
        current = self.model.get_values()[index]
        self.lines[index].setText(str(current))

    def on_spin_changed(self, index, value):
        self.model.set_value(index, value)
        current = self.model.get_values()[index]
        if self.spins[index].value() != current:
            self.spins[index].setValue(current)

    def on_slider_changed(self, index, value):
        self.model.set_value(index, value)
        current = self.model.get_values()[index]
        if self.sliders[index].value() != current:
            self.sliders[index].setValue(current)

    def update_from_model(self):
        self.update_count += 1
        values = self.model.get_values()
        print("Значения в UI изменены на: "+str(values)+" Изменение №" + str(self.update_count))
        for i in range(3):
            self.lines[i].setText(str(values[i]))
            self.spins[i].setValue(values[i])
            self.sliders[i].setValue(values[i])

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())