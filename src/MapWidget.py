from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import gmplot
from io import StringIO
from src.Map import Map


class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.api_key = "AIzaSyD1iK3XcJHRDowNirQ06qJiGZz-4bOJw7k"
        self.map = Map('0', '0', zoom=10, apikey=self.api_key)
        self.map.apikey = self.api_key

        html = self.map.get_html()
        html = "".join(html)

        self.setHtml(html)

    def update(self):
        pass
