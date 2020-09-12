from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QVBoxLayout, QLineEdit, QSlider, QLabel
from PIL import ImageGrab
from imageio import imread, imwrite
import seamcarving
import sys, os
from time import gmtime, strftime

scale = 0.5

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('INTLSNIP')
        self.setGeometry(200,200,300,300)
        self.initUI()
    def initUI(self):
        vboxLayout = QVBoxLayout()
        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(100,50)
        vboxLayout.addWidget(self.lineEdit)

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.move(100,20)
        self.slider.setValue(50)
        self.slider.setMinimum(1)

        self.slider.setMaximum(99)
        self.slider.setTickPosition(QSlider.TicksAbove)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.changedValue)
        vboxLayout.addWidget(self.slider)

        self.label = QLabel(self)
        self.label.move(100, 100)
        img_path = os.path.dirname(os.path.realpath(__file__)) + "/icon.jpg"
        self.label.setPixmap(QPixmap(img_path))
        self.label.setGeometry(50,50, 200, 200)
        vboxLayout.addWidget(self.label)


        menu = self.menuBar()
        action = menu.addMenu('Action')
        crop = QAction('Crop', self)
        crop.triggered.connect(self.trigger)
        help = menu.addMenu('Help')
        info = QAction('Info', self)
        action.addAction(crop)
        help.addAction(info)
    def changedValue(self):
        size = str(self.slider.value())
        global scale
        scale = self.slider.value()/100
        self.lineEdit.setText(size)

    def trigger(self):
        self.Crop = Crop()

class Crop(QMainWindow):
    def __init__(self, parent = None):
        super(Crop, self).__init__(parent)
        self.setStyleSheet('background-color: transparent;')
        self.setWindowOpacity(0.1)
        self.showFullScreen()
        self.COLOR = 'black'
        self.lineWidth = 2

        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.x1 = event.x()
        self.y1 = event.y()
        self.update()

    def mouseReleaseEvent(self, a0: QtGui.QMouseEvent):
        self.destroy()
        x1 = min(self.begin.x(), self.end.x())
        y1 = min(self.begin.y(), self.end.y())
        x2 = max(self.begin.x(), self.end.x())
        y2 = max(self.begin.y(), self.end.y())
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        dir = os.path.dirname(os.path.realpath(__file__))
        timestmp = strftime('%H%M%S', gmtime())
        self.filename =  dir + '/cropped/'+ timestmp + '.jpg'
        image.save(self.filename)
        input = imread(self.filename)
        print(scale)
        out = seamcarving.crop_c(input, scale)

        output = imwrite(dir + '/carved.jpg', out)
        print('done')


        application.show()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtGui.QPen(QtGui.QColor(self.COLOR), self.lineWidth))
        t = QtGui.QColor(255,255,255,255)
        qp.setBrush(t)
        rect = QtCore.QRect(self.begin, self.end)
        qp.drawRect(rect)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = App()
    application.show()
    sys.exit(app.exec_())

