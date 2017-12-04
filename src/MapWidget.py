from PyQt5.QtWebEngineWidgets import QWebEngineView
from src.Map import Map
import numpy as np
import pickle
from src.DBConnector import DBConnector
from src.utils import extract_multidim_results

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
                print('Could not load country cache')
                self.country_cache = {}

            try:
                with open(self.city_cache_path, 'rb') as f:
                    self.city_cache = pickle.load(f)
            except:
                print('Could not load city cache')
                self.city_cache = {}

        def get_country(self, name):
            extended_name = ('%s country' % name).title()
            try:
                location = self.country_cache[extended_name]
            except KeyError:
                location = Map.geocode(extended_name)
                if location is not None:
                    self.country_cache[extended_name] = location
                    with open(self.country_cache_path, 'wb') as f:
                        pickle.dump(self.country_cache, f)
            return location

        def get_city(self, name, country):
            extended_name = ('%s, %s' % (name, country)).title()
            try:
                location = self.city_cache[extended_name]
            except KeyError:
                location = Map.geocode(extended_name)
                if location is not None:
                    self.city_cache[extended_name] = location
                    with open(self.city_cache_path, 'wb') as f:
                        pickle.dump(self.city_cache, f)

            return location

    def __init__(self, parent=None):
        super().__init__(parent)
        self.map = None
        self.clear_map()
        self.location_cache = MapWidget.LocationCache()

    def display_processed_request(self, response, group):

        self.clear_map()
        action = response['action']
        result = response['result']
        print(response)

        # No data extracted
        if len(result) == 0:
            return

        title, result_array, keys = extract_multidim_results(result)

        # If dim is 1 then we know that it's just a value, so no grouping was done
        if len(keys) == 0:
            if 'geo-city' in response.keys() or 'geo-country' in response.keys():
                try:
                    location_name = response['geo-country'] if 'geo-country' in response.keys() else None
                    location_name = response['geo-city'] if 'geo-city' in response.keys() else location_name
                    location_name = location_name[0] if isinstance(location_name, list) else location_name
                    location = Map.geocode(location_name)
                    print(location)
                    self.map.marker(*location, color='red', title='%d' % result[0][0])
                except:
                    pass
                html = self.map.get_html()
                self.setHtml(html)

            else:
                # Maybe first field is a country/city
                try:
                    location_name = result[0][1]
                    location = Map.geocode(location_name)
                    self.map.marker(*location, color='red', title='%d' % result[0][0])
                except:
                    pass
                html = self.map.get_html()
                self.setHtml(html)


            return

        if 'geo-country' not in group and 'geo-city' not in group:
            return

        country = 'geo-country' in group

        if action in [DBConnector.A_comp, DBConnector.A_comp_grp_city, DBConnector.A_comp_grp_country]:

            # 1 D, Only 1D data supported
            if len(result_array.shape) == 1:
                if country:
                    self.display_grouping_country(result_array, keys[0])
                else:
                    self.display_grouping_city(result_array, keys[0], response['geo-country'])
        else:
            self.clear_map()

    def clear_map(self):
        self.map = Map(60, 5, zoom=4)
        html = self.map.get_html()
        self.setHtml(html)

    def display_grouping_country(self, result_array, names):
        for result, name in zip(result_array, names):
            try:
                lat, long = self.location_cache.get_country(name)
                self.map.marker(lat, long, color='red', title='%d' % result)
            except:
                print('Could not find a location for %s' % name)

        html = self.map.get_html()
        self.setHtml(html)

    def display_grouping_city(self, result_array, names, country):
        for result, name in zip(result_array, names):
            try:
                lat, long = self.location_cache.get_city(name, country)
                self.map.marker(lat, long, color='red', title='%d' % result)
            except:
                print('Could not find a location for %s' % name)

        html = self.map.get_html()
        self.setHtml(html)

