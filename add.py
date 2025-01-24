from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout,
                              QLabel, QLineEdit, QPushButton, QComboBox, QDateTimeEdit,
                              QInputDialog, QFrame, QHBoxLayout, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QFont, QIcon, QDoubleValidator
from PySide6.QtCore import QDateTime, Qt
import sys

class StyledLineEdit(QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #4361ee;
                background-color: white;
            }
        """)

class StyledComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #4361ee;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #495057;
                margin-right: 10px;
            }
        """)

class StyledDateTimeEdit(QDateTimeEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QDateTimeEdit {
                padding: 12px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: #f8f9fa;
                font-size: 14px;
            }
            QDateTimeEdit:focus {
                border: 2px solid #4361ee;
                background-color: white;
            }
        """)

class AddExpense(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Expense")
        self.setGeometry(100, 100, 600, 500)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel {
                color: #495057;
                font-size: 14px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Header
        header_label = QLabel("Add New Expense")
        header_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_label.setStyleSheet("color: #212529; margin-bottom: 20px;")
        main_layout.addWidget(header_label)

        # Form Container
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
            }
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(15)

        # Amount Field
        self.amount_input = StyledLineEdit("Enter amount")
        validator = QDoubleValidator(0.00, 999999.99, 2)
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.amount_input.setValidator(validator)
        form_layout.addRow("Amount ($):", self.amount_input)

        # Category Section
        category_layout = QHBoxLayout()
        self.category_dropdown = StyledComboBox()
        self.category_dropdown.addItems(["Food", "Transport", "Entertainment", "Utilities", "Other"])
        
        self.add_category_btn = QPushButton("+ Add")
        self.add_category_btn.setStyleSheet("""
            QPushButton {
                padding: 12px 20px;
                background-color: #e9ecef;
                border: none;
                border-radius: 8px;
                color: #495057;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #dee2e6;
            }
        """)
        self.add_category_btn.setCursor(Qt.PointingHandCursor)
        self.add_category_btn.clicked.connect(self.add_category)
        
        category_layout.addWidget(self.category_dropdown)
        category_layout.addWidget(self.add_category_btn)
        form_layout.addRow("Category:", category_layout)

        # Date/Time Field
        self.datetime_input = StyledDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.datetime_input.setCalendarPopup(True)
        form_layout.addRow("Date & Time:", self.datetime_input)

        # Notes Field
        self.notes_input = StyledLineEdit("Optional notes")
        form_layout.addRow("Notes:", self.notes_input)

        main_layout.addWidget(form_container)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        
        # Cancel Button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                color: #495057;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
            }
        """)
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        
        # Save Button
        self.save_btn = QPushButton("Save Expense")
        self.save_btn.setStyleSheet("""
            QPushButton {
                padding: 15px 30px;
                background-color: #4361ee;
                border: none;
                border-radius: 8px;
                color: white;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3b4fd3;
            }
        """)
        self.save_btn.setCursor(Qt.PointingHandCursor)
        self.save_btn.clicked.connect(self.save_expense)

        buttons_layout.addWidget(self.cancel_btn)
        buttons_layout.addWidget(self.save_btn)
        
        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def add_category(self):
        new_category, ok = QInputDialog.getText(
            self, 
            "Add Category",
            "Enter new category:",
            QLineEdit.Normal,
            ""
        )
        if ok and new_category.strip():
            self.category_dropdown.addItem(new_category.strip())
            self.category_dropdown.setCurrentText(new_category.strip())

    def save_expense(self):
        amount = self.amount_input.text()
        category = self.category_dropdown.currentText()
        date_time = self.datetime_input.dateTime().toString()
        notes = self.notes_input.text()
        print(f"Expense saved: Amount=${amount}, Category={category}, DateTime={date_time}, Notes={notes}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    add_expense_window = AddExpense()
    add_expense_window.show()

    sys.exit(app.exec())