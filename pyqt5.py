import os.path
import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QTextEdit, QWidget
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Interceptor(QWebEngineUrlRequestInterceptor):
    def interceptRequest(self, info):
        info.setHttpHeader(b"Accept-Language", b"en-US,en;q=0.9,es;q=0.8,de;q=0.7")


def mainPyQt5():
    CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
    filename = os.path.join(CURRENT_DIR, "index.html")
    app = QApplication(sys.argv)
    browser = QWebEngineView()

    interceptor = Interceptor()
    browser.page().profile().setUrlRequestInterceptor(interceptor)

    browser.load(QUrl.fromLocalFile(filename))
    browser.show()
    sys.exit(app.exec_())
    
    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

if __name__ == "__main__":
    mainPyQt5()