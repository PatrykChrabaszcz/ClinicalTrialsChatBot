import gmplot


class Map(gmplot.GoogleMapPlotter):

    class FakeFile:
        def __init__(self):
            self.lines = []

        def write(self, text):
            self.lines.append(text)

    def __init__(self, center_lat, center_lng, zoom, apikey=''):
        super().__init__(center_lat, center_lng, zoom, apikey)

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

        return lines

