from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                              QLabel, QHBoxLayout, QFrame, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
import sys

class DashboardButton(QPushButton):
    def __init__(self, text, icon_name=None):
        super().__init__(text)
        self.setFixedHeight(50)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                text-align: left;
                font-size: 14px;
                color: #495057;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)

class BalanceCard(QFrame):
    def __init__(self, title, amount, color):
        super().__init__()
        self.setFixedHeight(100)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("color: white; font-size: 14px;")
        
        amount_label = QLabel(amount)
        amount_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        
        layout.addWidget(title_label)
        layout.addWidget(amount_label)
        layout.setSpacing(5)

class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Personal Expense Tracker")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_label = QLabel("Dashboard")
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setStyleSheet("color: #212529;")
        main_layout.addWidget(header_label)

        # Balance Cards
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        balance_card = BalanceCard("Total Balance", "$2,450.00", "#4361ee")
        income_card = BalanceCard("Income", "$3,550.00", "#2ec4b6")
        expense_card = BalanceCard("Expenses", "$1,100.00", "#e63946")

        cards_layout.addWidget(balance_card)
        cards_layout.addWidget(income_card)
        cards_layout.addWidget(expense_card)

        main_layout.addLayout(cards_layout)

        # Navigation Section
        nav_label = QLabel("Quick Actions")
        nav_label.setFont(QFont("Arial", 16, QFont.Bold))
        nav_label.setStyleSheet("color: #212529; margin-top: 20px;")
        main_layout.addWidget(nav_label)

        # Navigation Buttons
        self.add_expense_btn = DashboardButton("Add New Expense")
        self.add_expense_btn.clicked.connect(self.add_expense_action)

        self.view_history_btn = DashboardButton("View Transaction History")
        self.view_history_btn.clicked.connect(self.view_history_action)

        self.summary_btn = DashboardButton("View Summary & Analytics")
        self.summary_btn.clicked.connect(self.summary_action)

        self.categories_btn = DashboardButton("Manage Categories")
        self.categories_btn.clicked.connect(self.categories_action)

        # Add buttons to layout
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.addWidget(self.add_expense_btn)
        buttons_layout.addWidget(self.view_history_btn)
        buttons_layout.addWidget(self.summary_btn)
        buttons_layout.addWidget(self.categories_btn)

        main_layout.addLayout(buttons_layout)

        # Add stretching space at the bottom
        main_layout.addStretch()

        self.setLayout(main_layout)

    def add_expense_action(self):
        print("Navigating to Add Expense")

    def view_history_action(self):
        print("Navigating to View History")

    def summary_action(self):
        print("Navigating to Summary")

    def categories_action(self):
        print("Navigating to Categories")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application-wide style
    app.setStyle("Fusion")
    
    home_window = Home()
    home_window.show()

    sys.exit(app.exec())