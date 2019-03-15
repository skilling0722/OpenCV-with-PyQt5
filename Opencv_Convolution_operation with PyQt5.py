import sys
import numpy as np
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import cv2

class Ui_MainWindow(QMainWindow):
    global img

    def __init__(self):
        super().__init__()

        self.init_Main_Ui()
        self.init_Menu_Ui()

    def init_Main_Ui(self):
        self.setObjectName("test")
        self.setEnabled(True)
        self.resize(1200, 700)
        self.setMinimumSize(QtCore.QSize(1200, 700))
        self.setMaximumSize(QtCore.QSize(1200, 700))

        self.image_label = QLabel(self)

        self.setCentralWidget(self.image_label)

        self.show()

    def init_Menu_Ui(self):
        global img
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        file_menu = menu_bar.addMenu('&File')  # &가 alt+F 메뉴 단축키 지정

        Exit_action = QAction('Exit', self)
        Exit_action.setShortcut('Ctrl+Q')
        Exit_action.triggered.connect(qApp.quit)

        Open_action = QAction('open', self)
        Open_action.setShortcut('Ctrl+O')
        Open_action.triggered.connect(self.read_file)

        file_menu.addAction(Open_action)
        file_menu.addAction(Exit_action)

        self.filter_menu = menu_bar.addMenu("&Filter")
        self.filter_menu.setEnabled(False)

        Sobel_action = QAction('Sobel filter', self)
        Sobel_action.setShortcut('Alt+1')
        Sobel_action.triggered.connect(
            lambda: self.Sobel_filter(img)
        )

        Prewitt_action = QAction('Prewitt filter', self)
        Prewitt_action.setShortcut('Alt+2')
        Prewitt_action.triggered.connect(
            lambda : self.Prewitt_filter(img)
        )

        Gaussian_action = QAction('Gaussian filter', self)
        Gaussian_action.setShortcut('Alt+3')
        Gaussian_action.triggered.connect(
            lambda : self.Gaussian_filter(img)
        )


        Canny_action = QAction('Canny filter', self)
        Canny_action.setShortcut('Alt+4')
        Canny_action.triggered.connect(
            lambda : self.Canny_filter(img)
        )

        LoG_action = QAction('LoG filter', self)
        LoG_action.setShortcut('Alt+5')
        LoG_action.triggered.connect(
            lambda : self.LoG_filter(img)
        )

        self.filter_menu.addAction(Sobel_action)
        self.filter_menu.addAction(Prewitt_action)
        self.filter_menu.addAction(Gaussian_action)
        self.filter_menu.addAction(Canny_action)
        self.filter_menu.addAction(LoG_action)


    def read_file(self):
        global img
        file_name = QFileDialog.getOpenFileName(self)

        if file_name[0] is not '':
            img0 = cv2.imread(file_name[0])

            img = cv2.cvtColor(img0, cv2.COLOR_BGR2RGB)

            self.reshow_image(img)
            print('aa')
            self.filter_menu.setEnabled(True)
        else:
            print('please put img')

    def save_image(self):
        print("save")

    def Sobel_filter(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

        sobel = img.copy()
        height = np.size(img, 0)
        width = np.size(img, 1)

        for i in range(width):
            for j in range(height):
                sobel[j, i] = np.minimum(255, np.round(np.sqrt(sobelx[j, i] * sobelx[j, i] + sobely[j, i] * sobely[j, i])))

        sobel = cv2.cvtColor(sobel, cv2.COLOR_GRAY2RGB)

        self.reshow_image(sobel)


    def Prewitt_filter(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])

        img_prewittx = cv2.filter2D(img, -1, kernelx)
        img_prewitty = cv2.filter2D(img, -1, kernely)

        Prewitt = cv2.cvtColor(img_prewittx + img_prewitty, cv2.COLOR_GRAY2RGB)
        self.reshow_image(Prewitt)


    def Gaussian_filter(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_smooth = cv2.GaussianBlur(img, (3, 3), 0)
        img_smooth = cv2.cvtColor(img_smooth, cv2.COLOR_GRAY2RGB)
        self.reshow_image(img_smooth)


    def Canny_filter(self, img):
        canny = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        canny = cv2.Canny(canny, 100, 150)
        canny = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)
        self.reshow_image(canny)


    def LoG_filter(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img_smooth = cv2.GaussianBlur(img, (3, 3), 0)
        laplacian = cv2.Laplacian(img_smooth, cv2.CV_8U, ksize=3)
        laplacian = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2RGB)
        self.reshow_image(laplacian)

    def reshow_image(self, cv_img):
        if cv_img is not None:
            self.image_label.resize(cv_img.shape[1], cv_img.shape[0])
            Q_img = QImage(cv_img.data, cv_img.shape[1], cv_img.shape[0], cv_img.shape[1] * 3, QImage.Format_RGB888)
            self.image_label.setPixmap(QPixmap.fromImage(Q_img))
        else:
            print("Image load failed")


    def exit(self):
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    sys.exit(app.exec_())