from PyQt5.QtWidgets import QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import os
import gmplot
from io import StringIO
from src.Map import Map


class MapWidget(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.location_cache = {}
        self.map = None
        self.clear_map()

    def get_location(self, location_name):
        try:
            location = self.location_cache[location_name]
        except KeyError:
            location = self.map.geocode(location_name)
            self.location_cache[location_name] = location

        return location

    def display_processed_request(self, response):
        self.clear_map()
        action = response['action']

        if action in ['count_place']:

            location_name = response['geo-country'] if 'geo-country' in response.keys() else None
            location_name = response['geo-city'] if 'geo-city' in response.keys() else location_name

            self.display_location(location_name, response['result'])

        elif action in ['count_grouping']:
            self.display_locations(response['result'])

        else:
            self.clear_map()

    def clear_map(self):
        self.map = Map(60, 5, zoom=4)
        html = self.map.get_html()
        self.setHtml(html)

    def display_location(self, location_name, result):
        self.map.marker(*self.get_location(location_name), color='red', title=result)
        html = self.map.get_html()
        self.setHtml(html)

    def display_locations(self, results):
        for key, value in results.items():
            self.map.marker(*self.get_location(key), color='red', title=value)
            html = self.map.get_html()
            self.setHtml(html)
