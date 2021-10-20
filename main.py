import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from step04 import Ui_MainWindow
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import requests
import csv
import openpyxl
import re
from openpyxl import load_workbook
from main2Crawler import *
import pocket_1
from del_excel_4 import *
from receipt_5 import *
from download_6 import *

#    form_class에 ui 파일을 로드한다.
form_class = uic.loadUiType("main2.ui")[0]

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_Craw.clicked.connect(self.crawling) # 크롤링
        self.btnInfoOK.clicked.connect(self.info) # 장바구니 1
        self.pushButton_2.clicked.connect(self.pocket) # 장바구니 반복
        self.btn_OpenFile.clicked.connect(self.openfile) # 파일 지정
        self.btn_del.clicked.connect(self.del_content) # 삭제
        self.pushButton_3.clicked.connect(self.receipt) # 영수증
        self.pushButton_4.clicked.connect(self.download) # 다운로드

    def crawling(self):
        name = self.Input_name_2.text()
        jumin1 = self.Input_jumin_3.text()
        jumin2 = self.Input_jumin_4.text()
        bub = self.Input_bub.text()
        main_Crawler(name, jumin1, jumin2, bub)

    def info(self, txt):
        name = self.Input_name.text()
        jumin1 = self.Input_jumin_1.text()
        jumin2 = self.Input_jumin_2.text()
        tel1 = self.Input_tel1.text()
        tel2 = self.Input_tel2.text()
        pocket_1.real_func(name, jumin1, jumin2, tel1, tel2)

    def pocket(self):
        pocket_1.basket()

    def openfile(self):
        filename = QFileDialog.getOpenFileName(self)
        fname = self.lbl_openfile.setText(filename[0])

    def del_content(self):
        file_path = self.lbl_openfile.text()
        delete_rows(50, file_path)

    def receipt(self):
        name = self.Input_name.text()
        jumin1 = self.Input_jumin_1.text()
        jumin2 = self.Input_jumin_2.text()
        tel1 = self.Input_tel1.text()
        tel2 = self.Input_tel2.text()
        func_receipt(name, jumin1, jumin2, tel1, tel2)

    def download(self):
        name = self.Input_name.text()
        jumin1 = self.Input_jumin_1.text()
        jumin2 = self.Input_jumin_2.text()
        tel1 = self.Input_tel1.text()
        tel2 = self.Input_tel2.text()
        func_download(name, jumin1, jumin2, tel1, tel2)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()

