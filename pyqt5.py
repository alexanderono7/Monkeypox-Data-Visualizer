import os.path
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QTextEdit, QWidget, QVBoxLayout
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")
    

class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        vbox = QVBoxLayout(self)

        # HTML STUFF STARTS HERE
        CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
        filename = os.path.join(CURRENT_DIR, "index.html")
        #app = QApplication(sys.argv)
        browser = QWebEngineView()

        interceptor = Interceptor()
        browser.page().profile().setUrlRequestInterceptor(interceptor)

        browser.load(QUrl.fromLocalFile(filename))

        vbox.addWidget(browser)
        # HTML STUFF ENDS HERE

        self.setLayout(vbox)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('QWebEngineView')
        self.show()

    def loadPage(self):

        with open('test.html', 'r') as f:

            html = f.read()
            self.webEngineView.setHtml(html)

def main():

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()