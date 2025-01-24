from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, 
                              QStackedWidget, QHBoxLayout, QFrame, QGridLayout)
from PySide6.QtCharts import (QChart, QChartView, QPieSeries, QBarSet, QBarSeries, 
                             QBarCategoryAxis, QValueAxis, QPieSlice)
from PySide6.QtGui import QFont, QPainter, QColor, QBrush, QPen
from PySide6.QtCore import Qt, QEvent
import sys
from manager import Manager

class StatCard(QFrame,Manager):
    def __init__(self, title, value, color):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        self.data = Manager
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px;")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("color: white; font-size: 22px; font-weight: bold;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)

class ChartNavigationButton(QPushButton):
    def __init__(self, text, is_next=True):
        super().__init__(text)
        self.setFixedSize(40, 40)
        direction = "right" if is_next else "left"
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 20px;
                font-size: 18px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #e9ecef;
            }}
        """)

class Summary(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Expense Summary")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_label = QLabel("Expense Summary")
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setStyleSheet("color: #212529;")
        main_layout.addWidget(header_label)

        # Stats Cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)

        total_card = StatCard("Total Expenses", "$2,450.00", "#4361ee")
        avg_card = StatCard("Daily Average", "$81.67", "#2ec4b6")
        top_card = StatCard("Highest Category", "Food ($820)", "#e63946")

        stats_layout.addWidget(total_card)
        stats_layout.addWidget(avg_card)
        stats_layout.addWidget(top_card)
        main_layout.addLayout(stats_layout)

        # Charts Container
        charts_container = QFrame()
        charts_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        charts_layout = QHBoxLayout(charts_container)

        # Chart Navigation and View
        nav_chart_layout = QHBoxLayout()
        
        self.prev_btn = ChartNavigationButton("←", False)
        self.prev_btn.clicked.connect(self.prev_chart)
        
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: white;")
        
        self.next_btn = ChartNavigationButton("→", True)
        self.next_btn.clicked.connect(self.next_chart)

        nav_chart_layout.addWidget(self.prev_btn)
        nav_chart_layout.addWidget(self.stacked_widget, 1)
        nav_chart_layout.addWidget(self.next_btn)

        charts_layout.addLayout(nav_chart_layout)
        main_layout.addWidget(charts_container)

        # Add Charts
        self.add_pie_chart()
        self.add_bar_chart()

        self.setLayout(main_layout)

    def add_pie_chart(self):
        # Create and style pie series
        self.pie_series = QPieSeries()
        
        # Add data with custom colors
        slice1 = self.pie_series.append("Food", 40)
        slice1.setColor(QColor("#4361ee"))
        
        slice2 = self.pie_series.append("Transport", 30)
        slice2.setColor(QColor("#2ec4b6"))
        
        slice3 = self.pie_series.append("Entertainment", 20)
        slice3.setColor(QColor("#e63946"))
        
        slice4 = self.pie_series.append("Utilities", 10)
        slice4.setColor(QColor("#ffb703"))

        # Make slices interactive
        for slice in self.pie_series.slices():
            # Connect hover events
            slice.hovered.connect(self.pie_slice_hovered)
            
            slice.setLabelVisible(True)
            slice.setLabelPosition(QPieSlice.LabelPosition.LabelOutside)
            percentage = f"{slice.percentage() * 100:.1f}%"
            slice.setLabel(f"{slice.label()}\n{percentage}")

        # Create and style chart
        self.pie_chart = QChart()
        self.pie_chart.addSeries(self.pie_series)
        self.pie_chart.setTitle("Expenses by Category")
        self.pie_chart.setTitleFont(QFont("Arial", 16, QFont.Bold))
        self.pie_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.pie_chart.legend().setVisible(False)

        # Create chart view
        chart_view = QChartView(self.pie_chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        self.stacked_widget.addWidget(chart_view)

    def pie_slice_hovered(self, is_hovering):
        slice = self.sender()
        if is_hovering:
            # Explode and highlight the hovered slice
            slice.setExploded(True)
            slice.setExplodeDistanceFactor(0.1)  # Increase separation
            
            # Add hover border
            slice.setBorderColor(QColor("#000000"))
            slice.setBorderWidth(2)
        else:
            # Reset slice when not hovering
            slice.setExploded(False)
            slice.setExplodeDistanceFactor(0)
            slice.setBorderWidth(0)

    def add_bar_chart(self):
        # Create and style bar series
        self.bar_set = QBarSet("Expenses")
        self.bar_set.setColor(QColor("#4361ee"))
        self.bar_set << 40 << 30 << 20 << 10

        self.bar_series = QBarSeries()
        self.bar_series.append(self.bar_set)

        # Create and style chart
        self.bar_chart = QChart()
        self.bar_chart.addSeries(self.bar_series)
        self.bar_chart.setTitle("Weekly Expenses")
        self.bar_chart.setTitleFont(QFont("Arial", 16, QFont.Bold))
        self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)

        # Hover effects for bars
        self.bar_series.barsetsAdded.connect(self.setup_bar_hover)

        # Set up axes
        categories = ["Week 1", "Week 2", "Week 3", "Week 4"]
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        axis_x.setTitleText("Weeks")
        
        axis_y = QValueAxis()
        axis_y.setTitleText("Amount ($)")
        axis_y.setRange(0, 50)

        self.bar_chart.addAxis(axis_x, Qt.AlignBottom)
        self.bar_chart.addAxis(axis_y, Qt.AlignLeft)
        self.bar_series.attachAxis(axis_x)
        self.bar_series.attachAxis(axis_y)

        # Create chart view
        chart_view = QChartView(self.bar_chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        
        # Enable hover tracking
        chart_view.setMouseTracking(True)
        chart_view.installEventFilter(self)
        
        self.stacked_widget.addWidget(chart_view)

    def setup_bar_hover(self):
        # Create a hover effect for bars
        for barset in self.bar_series.barSets():
            barset.setColor(QColor("#4361ee"))

    def eventFilter(self, obj, event):
        # Hover effect for bar chart
        if isinstance(obj, QChartView) and event.type() == QEvent.MouseMove:
            chart_view = obj
            chart = chart_view.chart()
            
            # Find the bar under the mouse
            bar_series = chart.series()[0]
            for i, bar_set in enumerate(bar_series.barSets()):
                # Modify bar appearance on hover
                bar_set.setColor(QColor("#2ec4b6") if bar_set.color() == QColor("#4361ee") else QColor("#4361ee"))
        
        return super().eventFilter(obj, event)

    def next_chart(self):
        current_index = self.stacked_widget.currentIndex()
        next_index = (current_index + 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(next_index)
        self.trigger_animation(next_index)

    def prev_chart(self):
        current_index = self.stacked_widget.currentIndex()
        prev_index = (current_index - 1) % self.stacked_widget.count()
        self.stacked_widget.setCurrentIndex(prev_index)
        self.trigger_animation(prev_index)

    def trigger_animation(self, index):
        if index == 0:
            self.pie_chart.setAnimationOptions(QChart.SeriesAnimations)
        elif index == 1:
            self.bar_chart.setAnimationOptions(QChart.SeriesAnimations)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    summary_window = Summary()
    summary_window.show()

    sys.exit(app.exec())