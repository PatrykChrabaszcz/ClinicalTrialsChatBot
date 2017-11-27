from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries, QHorizontalBarSeries
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QSize, Qt


class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QChartView.ScrollHandDrag)



    def database_response(self, response):
        action = response['action']
        status = response['status'] if 'status' in response.keys() else None
        location = response['location'] if 'location' in response.keys() else None
        disease = response['disease'] if 'disease' in response.keys() else None

        title = ''
        title += 'Disease: %s, ' % disease if disease is not None else ''
        title += 'Status: %s, ' % status if status is not None else ''
        title += 'Location: %s, ' % location if location is not None else ''

        if action in ['count_place']:
            self.display_single_value(response['result'])

        elif action in ['compare_cities', 'compare_countries', 'compare_diseases', 'compare_phases',
                        'count_place', 'count_grouping']:
            self.display_compare_lvl_1(title, response['result'])

    def display_single_value(self, results):
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(title)

        chart.removeAllSeries()
        series = QPieSeries()
        for key, value in response.items():
            series.append("%s (%d)" % (key, value), value)

        for slice in series.slices():
            slice.setLabelVisible()

        chart.addSeries(series)
        self.setChart(chart)

        chart.legend().hide()
        pass

    def display_compare_lvl_1(self, title, results):
        chart = QChart()
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)

        s = QBarSet("")
        axis = QBarCategoryAxis()
        labels_font = QFont()
        labels_font.setPixelSize(10)
        axis.setLabelsFont(labels_font)

        for key, value in sorted(results.items(), key=lambda c: c[1]):
            s.append(value)
            axis.append("%s (%s)" % (key.split(',')[0], value))

        series = QHorizontalBarSeries()
        series.append(s)
        chart.addSeries(series)
        chart.setAxisY(axis, series)
        chart.setMinimumHeight(25 * s.count())
        chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        chart.legend().hide()
        self.setChart(chart)
