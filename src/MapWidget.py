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
        self.map = Map.from_geocode('Freiburg', zoom=4)
        self.map.apikey = self.api_key

        code = self.map.geocode('Freiburg')
        self.map.heatmap([code[0]], [code[1]], 1, 10)

        code = self.map.geocode('Berlin')
        self.map.heatmap([code[0]], [code[1]], 1, 50)
        self.map.marker(code[0], code[1], title="500")

        html = self.map.get_html()
        html = "".join(html)


        self.setHtml(html)

    def update(self):
        pass
