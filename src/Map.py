import gmplot
import json
import requests


class Map(gmplot.GoogleMapPlotter):
    api_key = "AIzaSyD1iK3XcJHRDowNirQ06qJiGZz-4bOJw7k"

    class FakeFile:
        def __init__(self):
            self.lines = []

        def write(self, text):
            self.lines.append(text)

    def __init__(self, center_lat, center_lng, zoom):
        super().__init__(center_lat, center_lng, zoom, Map.api_key)

    @classmethod
    def geocode(self, location_string):
        try:
            geocode = requests.get(
                'https://maps.googleapis.com/maps/api/geocode/json?address="%s"&key=%s' %
                (location_string, Map.api_key))
            geocode = json.loads(geocode.text)
            print(geocode)
            latlng_dict = geocode['results'][0]['geometry']['location']
            return latlng_dict['lat'], latlng_dict['lng']
        except:
            return None

    def get_html(self):
        f = Map.FakeFile()
        lines = list()
        lines.append('<html>\n')
        lines.append('<head>\n')
        lines.append(
            '<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
        lines.append(
            '<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
        lines.append('<title>Google Maps - pygmaps </title>\n')
        if self.apikey:
            lines.append(
                '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false&key=%s"></script>\n' % self.apikey)
        else:
            lines.append(
                '<script type="text/javascript" src="https://maps.googleapis.com/maps/api/js?libraries=visualization&sensor=true_or_false"></script>\n')
        lines.append('<script type="text/javascript">\n')
        lines.append('\tfunction initialize() {\n')
        self.write_map(f)
        self.write_grids(f)
        self.write_points(f)
        self.write_paths(f)
        self.write_shapes(f)
        self.write_heatmap(f)
        lines.extend(f.lines)
        lines.append('\t}\n')
        lines.append('</script>\n')
        lines.append('</head>\n')
        lines.append(
            '<body style="margin:0px; padding:0px;" onload="initialize()">\n')
        lines.append(
            '\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
        lines.append('</body>\n')
        lines.append('</html>\n')

        return ''.join(lines)

    # We had to coment out img
    # We added Label
    def write_point(self, f, lat, lon, color, title):
        f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n' %
                (lat, lon))
        f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' %
                (self.coloricon % color))
        f.write('\t\tvar marker = new google.maps.Marker({\n')
        f.write('\t\ttitle: "%s",\n' % title)
        f.write('\t\tlabel: {text: "%s", fontSize: "10px"},\n' % title)
        #f.write('\t\ticon: img,\n')
        f.write('\t\tposition: latlng\n')
        f.write('\t\t});\n')
        f.write('\t\tmarker.setMap(map);\n')
        f.write('\n')