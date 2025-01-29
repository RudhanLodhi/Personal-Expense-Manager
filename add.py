import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout,
                              QLabel, QLineEdit, QPushButton, QComboBox, QDateTimeEdit,
                              QInputDialog, QFrame, QHBoxLayout, QMessageBox, QStyleFactory,
                              QListView,QCalendarWidget)
from PySide6.QtCore import QDateTime, Qt, QTimer
from manager import Manager

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
                color: #212529;
            }
            QLineEdit:hover {
                border: 2px solid #ced4da;
            }
            QLineEdit:focus {
                border: 2px solid #4361ee;
                background-color: white;
            }
            QLineEdit::placeholder {
                color: #6c757d;
            }
        """)

class StyledComboBox(QComboBox):
    def __init__(self):
        super().__init__()
        self.setView(QListView())
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)
        
        self.setStyleSheet("""
    QComboBox {
        padding: 8px 12px;
        border: 2px solid #e9ecef;
        border-radius: 6px;
        background-color: #f8f9fa;
        font-size: 14px;
        color: #212529;
        min-width: 200px;
        combobox-popup: 0;
    }
    QComboBox:hover {
        border: 2px solid #ced4da;
    }
    QComboBox:focus {
        border: 2px solid #4361ee;
        background-color: white;
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: center right;
        width: 36px;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
    }
    QListView {
        border: 2px solid #e9ecef;
        border-radius: 6px;
        background-color: white;
        outline: 0px;
        padding: 5px;
    }
    QListView::item {
        padding: 5px;
        border-radius: 3px;
        color: #212529; /* Ensure default text color */
        background-color: transparent; /* Transparent for unselected */
    }
    QListView::item:hover {
        background-color: #f8f9fa;
    }
    QListView::item:selected {
        background-color: #e9ecef;
        color: #212529; /* Ensure selected text is visible */
    }
""")

class StyledDateTimeEdit(QDateTimeEdit):
    def __init__(self):
        super().__init__()
        self.setCalendarPopup(True)
        
        calendar = self.calendarWidget()
        if calendar:
            calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
            calendar.setGridVisible(True)
            calendar.setFixedSize(350, 250) 
        
        self.setStyleSheet("""
            QDateTimeEdit {
                padding: 8px 12px;
                border: 2px solid #e9ecef;
                border-radius: 6px;
                background-color: #f8f9fa;
                font-size: 14px;
                color: #212529;
                min-width: 200px;
            }
            QDateTimeEdit:hover {
                border: 2px solid #ced4da;
            }
            QDateTimeEdit:focus {
                border: 2px solid #4361ee;
                background-color: white;
            }
            QDateTimeEdit::down-button {
                width: 20px;
                background: transparent;
            }
            QDateTimeEdit::up-button {
                width: 20px;
                background: transparent;
            }
            QDateTimeEdit::down-arrow, QDateTimeEdit::up-arrow {
                background: transparent;
                width: 0;
                height: 0;
            }
            
            QCalendarWidget {
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
            }
            QCalendarWidget QToolButton {
                height: 30px;
                color: black;
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                margin: 2px;
                padding: 2px 5px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #e9ecef;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth {
                qproperty-text: "<";
                background-color: transparent;
                border: none;
            }
            QCalendarWidget QToolButton#qt_calendar_nextmonth {
                qproperty-text: ">";
                background-color: transparent;
                border: none;
            }
            QCalendarWidget QToolButton#qt_calendar_prevmonth:hover,
            QCalendarWidget QToolButton#qt_calendar_nextmonth:hover {
                background-color: #e9ecef;
            }
            QCalendarWidget QMenu {
                width: 150px;
                background-color: white;
                border: 1px solid #e9ecef;
                border-radius: 6px;
            }
            QCalendarWidget QMenu::item {
                padding: 5px 10px;
                color: #212529;
            }
            QCalendarWidget QMenu::item:selected {
                background-color: #4361ee;
                color: white;
            }
            QCalendarWidget QSpinBox {
                border: 1px solid #e9ecef;
                border-radius: 4px;
                color: #212529;
                background-color: white;
                padding: 2px;
                min-width: 80px;
                
            }
            QCalendarWidget QSpinBox::up-button,
            QCalendarWidget QSpinBox::down-button {
                width: 20px;
                border: 1px solid #e9ecef;
                border-radius: 2px;
                background-color: #f8f9fa;
            }
            QCalendarWidget QSpinBox::up-button:hover,
            QCalendarWidget QSpinBox::down-button:hover {
                background-color: #e9ecef;
            }
            QCalendarWidget QSpinBox::up-arrow,
            QCalendarWidget QSpinBox::down-arrow {
                background: transparent;
                border: none;
                width: 0;
                height: 0;
            }
            /* Calendar cells */
            QCalendarWidget QAbstractItemView:enabled {
                color: blue;
                background-color: white;  /* Set background color for calendar days */
                selection-background-color: #4361ee;
                selection-color: white;
                border: none;
                outline: 0;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #adb5bd;
            }
            /* Navigation bar */
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: white;
                border-bottom: 1px solid #e9ecef;
                padding: 5px;
            }
        """)
class SuccessMessage(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                background-color: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        self.hide()

class AddExpense(QWidget):
    def __init__(self):
        super().__init__()
        self.manager = Manager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Add Expense")
        self.setGeometry(100, 100, 600, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: white;
            }
            QLabel {
                color: #495057;
                font-size: 14px;
            }
            QLabel#headerLabel {
                color: #212529;
                font-size: 24px;
                font-weight: bold;
                padding: 10px 0px;
                margin-bottom: 20px;
                border-bottom: 2px solid #e9ecef;
            }
            QLabel#formLabel {
                padding-right: 15px;  /* Add padding to align with input fields */
                min-width: 120px;    /* Set minimum width for labels */
                max-width: 120px;    /* Set maximum width for labels */
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Header
        header_label = QLabel("Add New Expense")
        header_label.setObjectName("headerLabel")  # Set object name for specific styling
        main_layout.addWidget(header_label)

        # Success Message
        self.success_message = SuccessMessage()
        main_layout.addWidget(self.success_message)

        # Form Container
        form_container = QFrame()
        form_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #e9ecef;
            }
        """)
        form_layout = QFormLayout(form_container)
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)  # Align labels to the right
        form_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)  # Allow fields to grow

        # Create labels with the formLabel object name
        amount_label = QLabel("Amount ($):")
        amount_label.setObjectName("formLabel")
        category_label = QLabel("Category:")
        category_label.setObjectName("formLabel")
        datetime_label = QLabel("Date & Time:")
        datetime_label.setObjectName("formLabel")
        notes_label = QLabel("Notes:")
        notes_label.setObjectName("formLabel")

        # Amount Field
        self.amount_input = StyledLineEdit("Enter amount")
        form_layout.addRow(amount_label, self.amount_input)

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
        form_layout.addRow(category_label, category_layout)

        # Date/Time Field
        self.datetime_input = StyledDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())
        self.datetime_input.setCalendarPopup(True)
        form_layout.addRow(datetime_label, self.datetime_input)

        # Notes Field
        self.notes_input = StyledLineEdit("Optional notes")
        form_layout.addRow(notes_label, self.notes_input)

        main_layout.addWidget(form_container)

        # Buttons Layout
        buttons_layout = QHBoxLayout()
        
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
        self.cancel_btn.clicked.connect(self.close)
        
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
            QPushButton:pressed {
                background-color: #2f3eb2;
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

    def show_success_message(self, message):
        self.success_message.setText(message)
        self.success_message.show()
        QTimer.singleShot(3000, self.success_message.hide)

    def clear_inputs(self):
        self.amount_input.clear()
        self.notes_input.clear()
        self.datetime_input.setDateTime(QDateTime.currentDateTime())

    def save_expense(self):
        try:
            amount = float(self.amount_input.text())
            category = self.category_dropdown.currentText()
            date_time = self.datetime_input.dateTime().toString("yyyy-MM-dd HH:mm:ss")
            notes = self.notes_input.text()

            if amount <= 0:
                QMessageBox.warning(self, "Invalid Amount", "Please enter a valid amount greater than 0.")
                return

            self.manager.add_entry(amount, date_time, category, notes)
            self.manager.export()

            self.show_success_message("Expense added successfully!")
            self.clear_inputs()

        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid amount.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))

    add_expense_window = AddExpense()
    add_expense_window.show()
    sys.exit(app.exec())