import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QMessageBox, QDialog, QLabel, QLineEdit, QDialogButtonBox, QComboBox
)

#first window you see
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #Window properties
        self.setWindowTitle('Garden Management App')
        self.resize(600, 600)

        #Layout
        layout = QVBoxLayout()

        #Buttons
        btn_input = QPushButton('Input Measurements for New Garden', self)
        btn_input.clicked.connect(self.open_indoor_outdoor_dialog)  #method call

        btn_update = QPushButton('Update Existing Garden', self)
        btn_update.clicked.connect(self.update_garden)              #method call

        #Add buttons to layout
        layout.addWidget(btn_input)
        layout.addWidget(btn_update)

        #Set layout for the main window
        self.setLayout(layout)

    #make new garden section
    def open_indoor_outdoor_dialog(self):
        #Open Indoor/Outdoor selection dialog
        dialog = IndoorOutdoorDialog(self)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #error detection needed
        if dialog.exec_() == QDialog.Accepted:          
            environment = dialog.get_selection()
            self.open_garden_dimensions_dialog(environment)     #method call
            
    #need a seperate call to get text selection
    def open_garden_dimensions_dialog(self, environment):
        # Open garden dimensions input dialog
        dialog = garden_dimensions_dialog(self)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #error detection needed
        if dialog.exec_() == QDialog.Accepted:
            garden_size = dialog.input_field.text()
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            #variables carry over and work
            #need output display now so new class above this
            #QMessageBox.information(
               # self,
               # 'Garden Input',
               # f'Environment: {environment}\nMeasurements: {garden_size}'
            #)
#???????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
            #in construction
            self.output_display = output_window(self.environment, self.garden_size)
            output_display.show()
    #update exsisting garden section
    def update_garden(self):
        # Action for "Update Existing Garden" button
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #update later, now is just a warning box
        QMessageBox.information(self, 'Update Garden', 'Update Me!')      

#first pop up 
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

#second pop up window
class garden_dimensions_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        #Dialog window properties
        self.setWindowTitle("Input Garden Measurements")
        self.setGeometry(300, 300, 300, 150)

        #Layout
        layout = QVBoxLayout(self)

        #Label --> text on screen pop up
        layout.addWidget(QLabel("Enter garden measurements (e.g., 10x20x30):", self))

        #Input Field --> what they are inputing 
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        #Dialog Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        
#Third pop up window
#output
class output_window(QWidget):

    def __init__(self, enviroment, garden_size):
        super().__init__()

        #Window properties
        self.setWindowTitle('Garden Management App')
        self.resize(600, 600)

        #Layout
        layout = QVBoxLayout()

        #Buttons
        btn_input = QPushButton('Input Measurements for New Garden', self)
        btn_input.clicked.connect(self.open_indoor_outdoor_dialog)  #method call

        btn_update = QPushButton('Update Existing Garden', self)
        btn_update.clicked.connect(self.update_garden)              #method call

        #Add buttons to layout
        layout.addWidget(btn_input)
        layout.addWidget(btn_update)

        #Set layout for the main window
        self.setLayout(layout)


#Main
#lauch MyApp method to start GUI procedure 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
