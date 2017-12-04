from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarCategoryAxis, QPieSeries, QHorizontalBarSeries, QAbstractBarSeries, QValueAxis
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtGui import QPainter, QFont, QPen, QColor
from src.DBConnector import DBConnector
import numpy as np
from src.LogWindow import logger
from src.utils import extract_multidim_results


class ChartWidget(QChartView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QChartView.ScrollHandDrag)

        self.title_font = QFont()
        self.title_font.setPixelSize(18)

    def display_processed_request(self, response, group):
        action = response['action']
        result = response['result']
        if action in [DBConnector.A_comp, DBConnector.A_comp_grp_country, DBConnector.A_comp_grp_city]:
            self.display_compare(result, group)

    def display_compare(self, result, group):
        # No data extracted
        if len(result) == 0:
            chart = QChart()
            chart.setTitle('NO DATA')
            self.setChart(chart)
            return

        t, result_array, new_keys = extract_multidim_results(result)

        chart = QChart()
        chart.setTitle(t.title())
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitleFont(self.title_font)
        chart.setPlotAreaBackgroundPen(QPen(QColor('red')))

        # Case with single value
        if len(new_keys) == 0:
            value = result[0][0]
            chart.setTitle(t.title() + ':\t %d' % value)
            elements = 1
            #
            # series = QHorizontalBarSeries()
            # axis = QBarCategoryAxis()
            # bar_set = QBarSet('')
            # axis.append("%s" % value)
            # bar_set.append(value)
            # series.append(bar_set)
            # chart.addSeries(series)
            # chart.setAxisY(axis, series)
            # elements = 1

        else:
            x_range = np.max(result_array)

            series = QHorizontalBarSeries()
            series.setLabelsFormat("<font color=\"black\"><b>@value<\\b><\\font>")
            series.setLabelsVisible(True)

            series.setLabelsPosition(QAbstractBarSeries.LabelsOutsideEnd)
            axis = QBarCategoryAxis()

            font = QFont()
            font.setPixelSize(1)

            chart.setFont(font)

            # 1D Data
            if len(result_array.shape) == 1:
                bar_set = QBarSet('')

                # We want to sort it such that rows with the most studies are on the top
                itr = sorted([(res, name) for (res, name) in zip(result_array, new_keys[0])])
                for res, name in itr:
                    # Take only the first part of the name if it has multiple parts
                    name = name.split(',')[0]
                    bar_set.append(res)
                    axis.append(name)

                series.append(bar_set)
                elements = result_array.shape[0]
                chart.legend().hide()

            # 2D Data
            elif len(result_array.shape) == 2:
                # Sort countries/cities such that the one with the most studies is on top
                itr = sorted([(res, name) for (res, name) in zip(result_array, new_keys[0])], key=lambda c: c[0].sum())

                bar_sets = [QBarSet(str(k)) for k in new_keys[1]]
                # Array with values for the 2nd category and name of the 1st dimension
                for res, name in itr:
                    name = name.split(',')[0]
                    for i, (r, name2) in enumerate(zip(res, new_keys[1])):
                        bar_sets[i].append(r)
                    axis.append(name)

                for bar_set in bar_sets:
                    series.append(bar_set)

                elements = result_array.shape[0] * result_array.shape[1]

            # TODO: Implement visualization for 3D data
            else:
                return

            chart.addSeries(series)
            chart.createDefaultAxes()
            chart.setAxisY(axis, series)
            chart.axisX().setRange(0, 1.1 * x_range)
            chart.axisX().applyNiceNumbers()

        chart.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.MinimumExpanding)
        chart.setMinimumHeight(30 * elements)
        self.setChart(chart)
