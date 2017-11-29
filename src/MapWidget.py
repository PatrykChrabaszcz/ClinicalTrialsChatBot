from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.Map import Map
import numpy as np
import pickle


class MapWidget(QWebEngineView):

    # We notice that querying Google API for many cities at the same time will be too slow.
    # Tries to cache the data in local files
    class LocationCache:
        def __init__(self):
            self.country_cache_path = 'resources/country_cache.p'
            self.city_cache_path = 'resources/city_cache.p'

            try:
                with open(self.country_cache_path, 'rb') as f:
                    self.country_cache = pickle.load(f)
            except:
                print('Could not load location cache')
                self.country_cache = {}

            try:
                with open(self.city_cache_path, 'rb') as f:
                    self.city_cache = pickle.load(f)
            except:
                print('Could not load location cache')
                self.city_cache = {}

        def get_country(self, name):
            extended_name = ('%s country' % name).title()
            try:
                location = self.country_cache[extended_name]
            except KeyError:
                location = Map.geocode(extended_name)
                self.country_cache[extended_name] = location
                with open(self.country_cache_path, 'wb') as f:
                    pickle.dump(self.country_cache, f)

            return location

        def get_city(self, name, country):
            extended_name = ('%s %s' % (name, country)).title()
            try:
                location = self.city_cache[name]
            except KeyError:
                location = Map.geocode(extended_name)
                self.city_cache[extended_name] = location
                with open(self.city_cache_path, 'wb') as f:
                    pickle.dump(self.city_cache, f)

            return location

    def __init__(self, parent=None):
        super().__init__(parent)
        self.map = None
        self.clear_map()
        self.location_cache = MapWidget.LocationCache()

    def display_processed_request(self, response):
        self.clear_map()
        action = response['action']

        if action in ['count_place']:

            location_name = response['geo-country'] if 'geo-country' in response.keys() else None
            location_name = response['geo-city'] if 'geo-city' in response.keys() else location_name

            self.display_country_count(location_name, response['result'])

        elif action in ['count_grouping']:
            self.display_grouping_country(response['result'])

        else:
            self.clear_map()

    def clear_map(self):
        self.map = Map(60, 5, zoom=4)
        html = self.map.get_html()
        self.setHtml(html)

    def display_country_count(self, name, count_result):
        long, lat = self.location_cache.get_country(name)
        self.map.marker(long, lat, color='red', title=count_result)
        html = self.map.get_html()
        self.setHtml(html)

    def display_city_count(self, name, count_result, country):
        long, lat = self.location_cache.get_city(name, country)
        self.map.marker(long, lat, color='red', title=count_result)
        html = self.map.get_html()
        self.setHtml(html)

    def display_grouping_country(self, results):
        for name, count_result in results.items():
            lat, long = self.location_cache.get_country(name)
            self.map.marker(lat, long, color='red', title=count_result)
            html = self.map.get_html()
            self.setHtml(html)

    def display_grouping_city(self, results, country):
        for name, count_result in results.items():
            lat, long = self.location_cache.get_city(name, country)
            self.map.marker(lat, long, color='red', title=count_result)
            html = self.map.get_html()
            self.setHtml(html)

