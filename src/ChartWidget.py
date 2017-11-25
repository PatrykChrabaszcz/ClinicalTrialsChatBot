from PyQt5.QtChart import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis


class ChartWidget(QChartView):
    def __init__(self):
        super().__init__()

        self.chart = QChart()
        self.chart.setTitle("Simple barchart example")
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        self.setChart(self.chart)

        s1 = QBarSet("Germany")
        s1.append([15])
        s1.append([30])
        s1.append([50])

        s2 = QBarSet("France")
        s2.append([10])
        s2.append([35])
        s2.append([41])
        series = QBarSeries()
        series.append(s1)
        series.append(s2)
        axis = QBarCategoryAxis()
        axis.append("2016")
        axis.append("2017")
        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.setAxisX(axis, series)