from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import gmplot


class MapWidget(QWebEngineView):
    def __init__(self, cache_dir):
        super().__init__()
        self.api_key = "AIzaSyD1iK3XcJHRDowNirQ06qJiGZz-4bOJw7k"
        self.gmap = gmplot.GoogleMapPlotter.from_geocode("San Francisco")
        self.gmap.apikey = self.api_key

        self.map_file = os.path.join(cache_dir, "map.html")
        self.gmap.draw(self.map_file)
        self.setUrl(QUrl("file://%s" % self.map_file))

    def update(self):
        pass
