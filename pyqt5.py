import datetime
import os.path
import sys

from PyQt5.QtCore import QUrl
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSlider, QLabel, QRadioButton
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import pyqtSlot, Qt, QRect

import sql_script as sql

class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")
    
#def getDate(x: int):

# Alexander Ono - 12/4/2022
class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.attr = 'cc'
        self.attrtext = 'Confirmed Cases'
        self.date = '2022-05-01'

        vbox = QVBoxLayout(self)

        # HTML STUFF STARTS HERE
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(CURRENT_DIR, "index.html")
        #app = QApplication(sys.argv)
        self.browser = QWebEngineView()
        browser = self.browser

        interceptor = Interceptor()
        browser.page().profile().setUrlRequestInterceptor(interceptor)

        browser.load(QUrl.fromLocalFile(filename))

        vbox.addWidget(browser)
        # HTML STUFF ENDS HERE

        self.sliderlabel = QLabel('', self) # Date label for slider
        
        self.sliderlabel.setFont(QFont('Arial',16))
        self.sliderlabel.move(190, 545)


        # Controller Objects
        '''
        button = QPushButton('PyQt5 button', self) # More for testing
        button.setToolTip('This is an example button')
        button.move(100,70)
        button.clicked.connect(lambda: self.on_click(browser)) # Sending browser as argument to button's activated function
        '''

        slider = QSlider(self)
        slider.setGeometry(QRect(190, 600, 570, 16))
        slider.setOrientation(Qt.Horizontal)
        slider.setRange(0,212)
        slider.valueChanged.connect(self.slidescale)

        # Radio Buttons
        
        x = 100
        y = 650
        self.radioButton_cc = QRadioButton(self)
        self.radioButton_cc.setGeometry(QRect(100, 650, 200, 20))
        self.radioButton_cc.toggled.connect(self.cc_selected)
        self.radioButton_cc.setText("Confirmed Cases")
        self.radioButton_cc.setChecked(True)

        self.radioButton_cd = QRadioButton(self)
        self.radioButton_cd.setGeometry(QRect(x, y+25, 200, 20))
        self.radioButton_cd.toggled.connect(self.cd_selected)
        self.radioButton_cd.setText("Confirmed Deaths")

        self.radioButton_nc = QRadioButton(self)
        self.radioButton_nc.setGeometry(QRect(x, y+50, 200, 20))
        self.radioButton_nc.toggled.connect(self.nc_selected)
        self.radioButton_nc.setText("New Cases")

        self.radioButton_nd = QRadioButton(self)
        self.radioButton_nd.setGeometry(QRect(x, y+75, 200, 20))
        self.radioButton_nd.toggled.connect(self.nd_selected)
        self.radioButton_nd.setText("New Deaths")


        self.setLayout(vbox)

        self.setGeometry(300, 300, 1000, 1000)
        self.setWindowTitle('CSE412 - DB Final Project, Group #18')
        self.show()

    def cc_selected(self, selected):
        if selected:
            self.attr = 'cc'
            self.attrtext = 'Confirmed Cases'
            self.browser.page().runJavaScript(f"setType(\'{self.attrtext}\')")
            sql.query_nations(attr=self.attr,date=self.date)
    def cd_selected(self, selected):
        if selected:
            self.attr = 'cd'
            self.attrtext = 'Confirmed Deaths'
            self.browser.page().runJavaScript(f"setType(\'{self.attrtext}\')")
            sql.query_nations(attr=self.attr,date=self.date)
    def nc_selected(self, selected):
        if selected:
            self.attr = 'nc'
            self.attrtext = 'New Cases'
            self.browser.page().runJavaScript(f"setType(\'{self.attrtext}\')")
            sql.query_nations(attr=self.attr,date=self.date)
    def nd_selected(self, selected):
        if selected:
            self.attr = 'nd'
            self.attrtext = 'New Deaths'
            self.browser.page().runJavaScript(f"setType(\'{self.attrtext}\')")
            sql.query_nations(attr=self.attr,date=self.date)



    @pyqtSlot()
    def on_click(self, browser):
        #brow.page().runJavaScript("updateMap(\'test_transition.csv\')")
        print('PyQt5 button click')
        browser.page().runJavaScript("updateMap(\'test_transition.csv\')")

    # Change date and update globe when moving slider. Also query the DB
    def slidescale(self, value) -> str:
        start_date = '05/01/2022'
        date_1 = datetime.datetime.strptime(start_date, "%m/%d/%Y")
        end_date = date_1 + datetime.timedelta(days=value)
        self.sliderlabel.setText(end_date.strftime("%m-%d-%Y"))
        self.sliderlabel.adjustSize()
        sql_date = end_date.strftime("%Y-%m-%d")
        self.date = sql_date
        sql.query_nations(attr=self.attr,date=sql_date)
        self.browser.page().runJavaScript("updateMap(\'buffer.csv\')")
        return end_date.strftime("%Y-%m-%d")


  

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()