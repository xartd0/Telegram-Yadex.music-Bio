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

api_id = '' # change here 
api_hash = '' # change here
old_yandex_data = ''
old_youtube_data = ''
media_url = 'https://www.youtube.com/' #change here

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
        global media_url
        super(MainWindow, self).__init__(*args, **kwargs)
        self.browser = QWebEngineView()
        page = WebEnginePage(self.browser)
        self.browser.setPage(page)
        self.browser.load(QUrl(media_url))
        self.setCentralWidget(self.browser)
        self.browser.loadFinished.connect(self.onLoadFinished)

    def injectjs(self, code, dist):
        self.browser.page().runJavaScript(code, dist)

    def check(self):
        if 'youtube.com/watch' in self.browser.url().toString():
            self.injectjs('var player = document.getElementById("movie_player"); if (player) true; else false;', self.check_youtube_data)
        else:
            self.injectjs("externalAPI.getCurrentTrack()", self.get_yandex_data)

    def get_yandex_data(self, data):
        self.data=data
        if self.data is not None:
            change_bio(f"Слушает ({self.data['artists'][0]['title']} - {self.data['album']['title']})")

    def check_youtube_data(self, data):
        self.data=data
        if self.data == True:
            self.injectjs('player.getVideoData()', self.get_youtube_data)

    def get_youtube_data(self, data):
        self.data = data 
        video = f"Смотрит ({self.data['author']} - {self.data['title']})"
        global old_youtube_data
        if video != old_youtube_data: 
            client(UpdateProfileRequest(
                        about=video
                    ))
            old_youtube_data = video
            print('Bio changed')
        
            
    def onLoadFinished(self, ok):
        if ok:
            setInterval(1.0, self.check)

def setInterval(timer, task):
    isStop = task()
    if not isStop:
        Timer(timer, setInterval, [timer, task]).start()

def change_bio(track):
    global old_yandex_data
    if track != old_yandex_data: 
        client(UpdateProfileRequest(
                    about=track
                ))
        old_yandex_data = track
        print('Bio changed')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    w.setWindowTitle('Music RPC')
    w.show()
    sys.exit(app.exec_())  
