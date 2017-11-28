from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries, QHorizontalBarSeries
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtCore import QSize, Qt


class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QChartView.ScrollHandDrag)

        self.title_font = QFont()
        self.title_font.setPixelSize(18)

    def display_processed_request(self, response):
        action = response['action']

        keys = ['disease', 'phase', 'status', 'location']

        title = ["%s: %s" % (key.title(), response[key]) for key in keys if key in response.keys()]
        title = ' | '.join(title)

        print(action)

        if action in ['count_place']:
            self.display_single_value(title, response['result'])

        elif action in ['compare_cities', 'compare_countries', 'compare_diseases', 'compare_phases',
                        'count_place', 'count_grouping']:
            self.display_compare_lvl_1(title, response['result'])

    def display_single_value(self, title, results):
        series = QPieSeries()
        series.append("%s" % results, results)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitleFont(self.title_font)
        chart.setTitle(title)

        self.setChart(chart)

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
