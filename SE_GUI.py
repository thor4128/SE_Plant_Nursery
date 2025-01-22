import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QInputDialog, QMessageBox, QDialog, QLabel, QLineEdit, QDialogButtonBox
)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window properties
        self.setWindowTitle('Garden Management App')
        self.setGeometry(100, 100, 400, 300)

        # Layout
        layout = QVBoxLayout()

        # Buttons
        btn_input = QPushButton('Input Measurements for New Garden', self)
        btn_input.clicked.connect(self.open_input_dialog)

        btn_update = QPushButton('Update Existing Garden', self)
        btn_update.clicked.connect(self.update_garden)

        # Add buttons to layout
        layout.addWidget(btn_input)
        layout.addWidget(btn_update)

        # Set layout for the main window
        self.setLayout(layout)

    def open_input_dialog(self):
        dialog = InputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            # Retrieve user input
            garden_size = dialog.input_field.text()
            QMessageBox.information(self, 'Garden Input', f'You entered: {garden_size}')

    def update_garden(self):
        # Action for "Update Existing Garden" button
        QMessageBox.information(self, 'Update Garden', 'Feature: Update Existing Garden!')


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Dialog properties
        self.setWindowTitle("Input Garden Measurements")
        self.setGeometry(200, 200, 300, 150)

        # Layout
        layout = QVBoxLayout(self)

        # Message label
        message = QLabel("Please enter the measurements for your new garden in meters (e.g., 10x20x30, Height, Width, Length):", self)
        layout.addWidget(message)

        # Input field
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        # Dialog buttons (OK and Cancel)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)


# Main block
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
