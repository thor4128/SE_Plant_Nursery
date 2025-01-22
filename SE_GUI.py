import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QDialog, QLabel, QLineEdit, QDialogButtonBox, QComboBox
)


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window properties
        self.setWindowTitle('Garden Management App')
        self.resize(600, 600)

        # Layout
        layout = QVBoxLayout()

        # Buttons
        btn_input = QPushButton('Input Measurements for New Garden', self)
        btn_input.clicked.connect(self.open_indoor_outdoor_dialog)

        btn_update = QPushButton('Update Existing Garden', self)
        btn_update.clicked.connect(self.update_garden)

        # Add buttons to layout
        layout.addWidget(btn_input)
        layout.addWidget(btn_update)

        # Set layout for the main window
        self.setLayout(layout)

    def open_indoor_outdoor_dialog(self):
        # Open Indoor/Outdoor selection dialog
        dialog = IndoorOutdoorDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            environment = dialog.get_selection()
            self.open_garden_dimensions_dialog(environment)

    def open_garden_dimensions_dialog(self, environment):
        # Open garden dimensions input dialog
        dialog = InputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            garden_size = dialog.input_field.text()
            QMessageBox.information(
                self,
                'Garden Input',
                f'Environment: {environment}\nMeasurements: {garden_size}'
            )

    def update_garden(self):
        # Action for "Update Existing Garden" button
        QMessageBox.information(self, 'Update Garden', 'Feature: Update Existing Garden!')


class IndoorOutdoorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Dialog properties
        self.setWindowTitle("Select Environment")
        self.setGeometry(300, 300, 300, 150)

        # Layout
        layout = QVBoxLayout(self)

        # ComboBox
        self.combo_box = QComboBox(self)
        self.combo_box.addItem("Indoor")
        self.combo_box.addItem("Outdoor")

        # Add ComboBox and Label to Layout
        layout.addWidget(QLabel("Please select the environment:", self))
        layout.addWidget(self.combo_box)

        # Dialog buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_selection(self):
        # Return selected environment
        return self.combo_box.currentText()


class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Dialog properties
        self.setWindowTitle("Input Garden Measurements")
        self.setGeometry(300, 300, 300, 150)

        # Layout
        layout = QVBoxLayout(self)

        # Label
        layout.addWidget(QLabel("Enter garden measurements (e.g., 10x20x30):", self))

        # Input Field
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        # Dialog Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)


# Main Block
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
