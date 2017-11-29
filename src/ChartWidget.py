from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QPieSeries, QHorizontalBarSeries
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtWidgets import QSizePolicy
import numpy as np
from src.LogWindow import logger


class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QChartView.ScrollHandDrag)

        self.title_font = QFont()
        self.title_font.setPixelSize(18)

    def display_processed_request(self, response):
        action = response['action']

        #keys = ['disease', 'phase', 'status', 'geo-country', 'geo-city']

        #title = ["%s: %s" % (key.title(), response[key]) for key in keys if key in response.keys()]
        #title = ' | '.join(title)

        #logger.log('ChartWidget: Action to display %s' % action)

        if action in ['compare']:
            self.display_compare(response['result'])

        elif action in ['compare_cities', 'compare_countries', 'compare_diseases', 'compare_phases',
                         'count_place', 'count_grouping_city', 'count_grouping_country']:
            self.display_compare_lvl_1(response['result'])

    def display_compare(self, result):
        print(result)
        dim = len(result[0])

        keys = []
        for d in range(1, dim):
            keys.append(list(set([r[d] for r in result])))

        t = []

        new_keys = []
        indices = []
        for i, s in enumerate(keys):
            if len(s) == 1:
                t.append(s[0])
            else:
                new_keys.append(s)
                indices.append(i+1)

        print('Title %s' % t)
        print(new_keys)
        dim = len(new_keys)

        chart = QChart()
        chart.setTitle(' '.join(t).title())
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitleFont(self.title_font)

        # Case with single value
        if len(new_keys) == 0:
            value = result[0][0]

            series = QPieSeries()
            series.append("%s" % value, value)

            chart.addSeries(series)

        else:
            # Right now we do not handle more dimensions
            if len(new_keys) > 2:
                return

            result_array = np.zeros(shape=[len(k) for k in new_keys])
            print(result_array)
            for r in result:
                index = []
                value = r[0]
                for d in range(len(new_keys)):
                    index.append(new_keys[d].index(r[indices[d]]))

                result_array[tuple(index)] = value

            series = QHorizontalBarSeries()
            axis = QBarCategoryAxis()

            print(result_array)
            for i in range(result_array.shape[0]):
                if len(result_array.shape) >= 2:
                    print('New Bar set')
                    bar_set = QBarSet(new_keys[0][i])
                    for j in range(result_array.shape[1]):
                        bar_set.append(result_array[i][j])
                        axis.append(new_keys[1][j])
                else:
                    bar_set = QBarSet(new_keys[0][i])
                    bar_set.append(result_array[i])
                    axis.append('')

                series.append(bar_set)

            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAxisY(axis, series)

        self.setChart(chart)

    def display_compare_lvl_1(self, results):
        print(results)
        # chart = QChart()
        # chart.setAnimationOptions(QChart.SeriesAnimations)
        #
        # s = QBarSet("")
        # axis = QBarCategoryAxis()
        # labels_font = QFont()
        # labels_font.setPixelSize(10)
        # axis.setLabelsFont(labels_font)
        #
        # for key, value in sorted(results.items(), key=lambda c: c[1]):
        #     s.append(value)
        #     axis.append("%s (%s)" % (key.split(',')[0], value))
        #
        # series = QHorizontalBarSeries()
        # series.append(s)
        # chart.addSeries(series)
        # chart.setAxisY(axis, series)
        # chart.setMinimumHeight(25 * s.count())
        # chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        # chart.legend().hide()
        # self.setChart(chart)
