from ast import arg
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from threading import Thread
from threading import Timer
from telethon import TelegramClient, events, sync
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from telethon import functions, types
from telethon.tl.functions.account import UpdateProfileRequest
import asyncio 


api_id = 'YOUR API_ID https://my.telegram.org/apps'
api_hash = 'YOUR API_HASH https://my.telegram.org/apps'

client = TelegramClient('session_name', api_id, api_hash)
client.start()

class WebEnginePage(QWebEnginePage):

    def createWindow(self, _type):
        page = WebEnginePage(self)
        page.urlChanged.connect(self.on_url_changed)
        return page

    @pyqtSlot(QUrl)
    def on_url_changed(self, url):
        page = self.sender()
        self.setUrl(url)
        page.deleteLater()

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        page = WebEnginePage(self.browser)
        self.browser.setPage(page)
        self.browser.load(QUrl("https://music.yandex.ru/home"))
        self.setCentralWidget(self.browser)
        self.browser.loadFinished.connect(self.onLoadFinished)

    def check(self):
        track = self.browser.page().runJavaScript("externalAPI.getCurrentTrack()", self.getdata)

    def getdata(self, data):
        self.data=data
        if self.data is not None:
            change_bio(f"Слушает ({self.data['artists'][0]['title']} - {self.data['album']['title']})")

    def onLoadFinished(self, ok):
        if ok:
            setInterval(1.0, self.check)

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()

def change_bio(track):
    client(UpdateProfileRequest(
                about=track
            ))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle('Music RPC')
    w.show()
    sys.exit(app.exec_())  
