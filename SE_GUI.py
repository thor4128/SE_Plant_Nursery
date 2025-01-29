import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QHBoxLayout, QPushButton, QMessageBox, QDialog, QLabel, QLineEdit, QDialogButtonBox, QComboBox
)



#first window you see
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        #messing around with scope leave this for now
        self.output_display = None
    def initUI(self):
        #Window properties
        self.setWindowTitle('Garden Management App')
        font = QFont('Verdana', 18, QFont.Bold)  # 'Verdana' font in bold
        

        #self.setGeometry(0, 0, 1800, 800)
        self.resize(1500,700)

        #main_layout = QHBoxLayout()
        #Layout
        layout = QVBoxLayout()

        #Buttons
        btn_input = QPushButton('Input Measurements for New Garden', self)
        btn_input.clicked.connect(self.open_indoor_outdoor_dialog)
        btn_input.setFixedSize(700, 250)

        btn_update = QPushButton('Update Existing Garden', self)
        btn_update.clicked.connect(self.update_garden)
        btn_update.setFixedSize(700, 250)
        
        btn_new = QPushButton('Insert New Feature', self)
        btn_new.clicked.connect(self.update_garden)
        btn_new.setFixedSize(700, 250)
        
         # Add buttons to the layout
        layout.addWidget(btn_input)
        layout.addWidget(btn_update)
        layout.addWidget(btn_new)
        
        # Apply this font to the button
        btn_input.setFont(font)
        btn_update.setFont(font)
        btn_new.setFont(font)
        
        # Style the buttons using stylesheets
        btn_input.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;  /* Green background */
            color: white;               /* White text */
            border: 2px solid #3E8E41;  /* Dark green border */
            border-radius: 12px;        /* Rounded corners */
            padding: 10px 24px;         /* Padding inside the button */
            font-size: 24px;            /* Font size */
        }
        QPushButton:hover {
            background-color: #45a049;  /* Lighter green when hovered */
            border: 2px solid #3c8033;  /* Darker border when hovered */
        }
        QPushButton:pressed {
            background-color: #2E8B57;  /* Even darker green when pressed */
            border: 2px solid #2a7030;  /* Darker border when pressed */
        }
    """)

        btn_update.setStyleSheet("""
        QPushButton {
            background-color: #008CBA;  /* Blue background */
            color: white;               /* White text */
            border: 2px solid #007B9A;  /* Darker blue border */
            border-radius: 12px;        /* Rounded corners */
            padding: 10px 24px;         /* Padding inside the button */
            font-size: 24px;            /* Font size */
        }
        QPushButton:hover {
            background-color: #007B9A;  /* Darker blue when hovered */
            border: 2px solid #005F73;  /* Darker border when hovered */
        }
        QPushButton:pressed {
            background-color: #005F73;  /* Even darker blue when pressed */
            border: 2px solid #004E5A;  /* Darker border when pressed */
        }
    """)

        btn_new.setStyleSheet("""
        QPushButton {
            background-color:#FFC72C;  /* yellow background */
            color: white;               /* White text */
            border: 2px solid #E0AC25;  /* Darker yellow border */
            border-radius: 12px;        /* Rounded corners */
            padding: 10px 24px;         /* Padding inside the button */
            font-size: 24px;            /* Font size */
        }
        QPushButton:hover {
            background-color: #E0AC25;  /* Darker yellow when hovered */
            border: 2px solid #E0AC25;  /* Darker border when hovered */
        }
        QPushButton:pressed {
            background-color:#C9921F;  /* Even darker yellow when pressed */
            border: 2px solid#C9921F;  /* Darker border when pressed */
        }
    """) 

        # Align the buttons to the top-left of the window
        layout.setAlignment(btn_input, Qt.AlignTop | Qt.AlignLeft)
        layout.setAlignment(btn_update, Qt.AlignTop | Qt.AlignLeft)
        layout.setAlignment(btn_new, Qt.AlignTop | Qt.AlignLeft)
        
        # --- Right Side: Image ---
        #image_label = QLabel()
        #pixmap = QPixmap('plant.png')  # Replace with your image file path
        #pixmap = pixmap.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #image_label.setPixmap(pixmap)
        #image_label.setAlignment(Qt.AlignCenter)

        # --- Add Layouts to Main Layout ---
        #main_layout.addLayout(layout)  # Add buttons on the lefts
        #main_layout.addWidget(image_label)   # Add image on the right

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
    def open_garden_dimensions_dialog(self, enviroment):
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
            self.load_information_for_output(enviroment, garden_size)
            
    #load inputs method for output display
    def load_information_for_output(self, enviroment, garden_size):
        print("im here 1")
        self.output_display = output_window(enviroment, garden_size)
        print("im here 2")
        self.output_display.show()
        
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
    def __init__(self, environment, garden_size, parent=None):
        super().__init__(parent)

        #Window properties
        self.setWindowTitle('Recommendations')
        self.resize(600, 600)

        #Layout
        layout = QVBoxLayout()

        #Add labels to display the environment and garden size
        layout.addWidget(QLabel(f"Environment: {environment}", self))
        layout.addWidget(QLabel(f"Garden Measurements: {garden_size}", self))

        #Set layout for the main window
        self.setLayout(layout)


#Main
#lauch MyApp method to start GUI procedure 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
