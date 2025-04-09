#Author Kody Ryant
#Software Engineering
#GUI for control over selection of garden bed size and enviroment to send to C# file to 
#give plant recomendations for that garden bed on an output window of this GUI

import sys
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,QHBoxLayout, QPushButton, QMessageBox, QDialog, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QSplashScreen
)
import subprocess
import json
import math
#import SE_backend.cs

#first window you see
class first_window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

        #messing around with scope leave this for now
        self.output_display = None
        
    def initUI(self):
        #Window properties
        self.setWindowTitle('Plant Planner')
        font = QFont('Verdana', 22, QFont.Bold)  # 'Verdana' font in bold
        
        #self.setGeometry(0, 0, 1800, 800)
        self.setFixedSize(800,550)

        #main_layout = QHBoxLayout()
        #Layout
        layout = QVBoxLayout()
        
        self.setStyleSheet("background-color:#D4F4DD; color:#556B2F;")

        #Buttons
        btn_input = QPushButton('Input Measurements for New Garden', self)
        btn_input.clicked.connect(self.open_indoor_outdoor_dialog)
        btn_input.setFixedSize(700, 250)

        btn_update = QPushButton('Update Existing Garden', self)
        btn_update.clicked.connect(self.update_garden)
        btn_update.setFixedSize(700, 250)
        
         # Add buttons to the layout
        layout.addWidget(btn_input)
        layout.addWidget(btn_update)
        
        # Apply this font to the button
        btn_input.setFont(font)
        btn_update.setFont(font)
        
        # Style the buttons using stylesheets
        btn_input.setStyleSheet(
        '''
            QPushButton {
                background-color: #008CBA;  /* Blue background */
                color: white;               /* White text */
                border: 2px solid #007B9A;  /* Darker blue border */
                border-radius: 12px;        /* Rounded corners */
                padding: 5px 12px;         /* Padding inside the button */
                font-size: 16px;            /* Font size */
            }
            QPushButton:hover {
                background-color: #007B9A;  /* Darker blue when hovered */
                border: 2px solid #005F73;  /* Darker border when hovered */
            }
            QPushButton:pressed {
                background-color: #005F73;  /* Even darker blue when pressed */
                border: 2px solid #004E5A;  /* Darker border when pressed */
            }
        '''
            
        )

        btn_update.setStyleSheet(
        '''
            QPushButton {
                background-color: #008CBA;  /* Blue background */
                color: white;               /* White text */
                border: 2px solid #007B9A;  /* Darker blue border */
                border-radius: 12px;        /* Rounded corners */
                padding: 5px 12px;         /* Padding inside the button */
                font-size: 16px;            /* Font size */
            }
            QPushButton:hover {
                background-color: #007B9A;  /* Darker blue when hovered */
                border: 2px solid #005F73;  /* Darker border when hovered */
            }
            QPushButton:pressed {
                background-color: #005F73;  /* Even darker blue when pressed */
                border: 2px solid #004E5A;  /* Darker border when pressed */
            }
        '''
            
        )


        # Align the buttons to the top-left of the window
        layout.setAlignment(btn_input, Qt.AlignCenter | Qt.AlignTop)
        layout.setAlignment(btn_update, Qt.AlignCenter | Qt.AlignBottom)
        
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
        while True:
        
        # Open garden dimensions input dialog
            dialog = garden_dimensions_dialog(self)
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if dialog.exec_() == QDialog.Accepted:
                garden_size = dialog.input_field.text()
            else:
                break
            
            #error detection
            valid_dimensions = True
            #change chars to lowercase
            lower_garden_size = garden_size.lower()
            #split the string into an array of the three dimensions
            char_array = lower_garden_size.split('x')
             #check array
            #print(char_array)
            #if the array doesn't have 3 dimensions it's invalid
            if len(char_array) != 3:
                valid_dimensions = False

            #if any of the dimensions are missing it's invalid
            for i in char_array:
             if i == "" or i == " ":
                valid_dimensions = False
  
            #try catch block to see if the 3 dimension values are floats       
            try:
                float_array = [float(value) for value in char_array]
                #make sure the float is not negative
                for i in float_array:
                 if i < 0:
                     valid_dimensions = False
            #if not a float the dimensions are false
            except ValueError:
             valid_dimensions = False
                
            if not valid_dimensions:
                 #print("The dimensions you entered are invalid, please enter correct values.")
                 dialog = invalid_dimensions(self)
                 dialog.exec_() == QDialog.Accepted
            else:
                self.load_information_for_output(enviroment, lower_garden_size)
                break

            #variables carry over and work
            #need output display now so new class above this
            #QMessageBox.information(
               # self,
               # 'Garden Input',
               # f'Environment: {environment}\nMeasurements: {garden_size}'
            #)
            #in construction
            #self.load_information_for_output(enviroment, garden_size)
            
    #load inputs method for output display
    def load_information_for_output(self, enviroment, garden_size):
        #print("im here 1")
        self.output_display = output_window(enviroment, garden_size)
        #print("im here 2")
        self.output_display.show()
        
    #update exsisting garden section
    def update_garden(self):
        # Action for "Update Existing Garden" button

        #update later, now is just a warning box
        QMessageBox.information(self, 'Update Garden', 'Update Me!')      

#invalid dimensions pop up window
class invalid_dimensions(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
    
     # Dialog properties
        self.setWindowTitle("Invalid Dimensions")
        self.setGeometry(300, 300, 300, 150)
        
    # Layout
        layout = QVBoxLayout(self)
        
    #Label --> text on screen pop up
        layout.addWidget(QLabel("The dimensions that were entered are invalid, please enter valid dimesnions.", self))
        
    #Dialog Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok, self)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

        self.setLayout(layout)

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
        layout.addWidget(QLabel("Enter garden measurements in meters(e.g., 10x20x30):", self))

        #Input Field --> what they are inputing 
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)

        #Dialog Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        
        
#integrated code here with plant panel
class plant_panel(QWidget):
    
    i = -1
    name = None
    parent = None
    alias = None
    image = None
    plantSize = float(100)
    environment = None
    count = 0
    selectButton = None
    deselectButton = None
    nameLabel = None
    countLabel = None
    errorMsg = None
    header = None
    gardenSizeRemaining = float(100)
    
    def __init__(self, parent, i, name, alias, image, plantSize, environment, count):
        super().__init__(parent)
        self.parent = parent
        self.i = i
        self.name = name
        self.alias = alias
        self.image = image
        self.plantSize = plantSize
        self.environment = environment
        self.count = count
        self.setObjectName(f"{name}")
        
    def plantDecrement(self):
        if self.i == -1: return
        
        if self.count <= 0:
            return
        
        plant_panel.errorMsg.setText("")
        
        plant_panel.gardenSizeRemaining += self.plantSize
        plant_panel.header.setText(f"Here are the plants we've selected -- Room Remaining: {round(plant_panel.gardenSizeRemaining, 2)}")
        self.count -= 1
        
        self.nameLabel.setText(f"{self.count}x {self.name}")
        self.countLabel.setText(f"{self.count}")
        
        if self.count == 0:
            
            #print(2)
            self.setStyleSheet("background-color:none; color:#556B2F;")
            """self.setStyleSheet('''
                             #PlantPanel {
                                 background-color:#D4F4DD;
                                 color:#556B2F;
                                 border: none;
                             }
                             
                             ''')"""
    
    def plantIncrement(self):
        #print(2)
        #print(0)
        if self.i == -1: return
        if plant_panel.gardenSizeRemaining - self.plantSize < 0:
            # add message and cancel
            
            #errorMsg = QLabel("Garden Size Exceeded!", self)
            #errorMsg.setStyleSheet("color: red; font-size: 12px;")
            plant_panel.errorMsg.setText("This plant doesn't fit!")
            return
        
        #print(1)
        plant_panel.errorMsg.setText("")
        # otherwise do normal stuff
        plant_panel.gardenSizeRemaining -= self.plantSize
        plant_panel.header.setText(f"Here are the plants we've selected -- Room Remaining: {round(plant_panel.gardenSizeRemaining, 2)} meters")

        self.count += 1
        #print(2)
        self.nameLabel.setText(f"{self.count}x {self.name}")
        #print(3)
        self.countLabel.setText(f"{self.count}")
        #print(4)
        if self.count >= 1:
            #print(1)
            #self.setStyleSheet("background-color:#D4F4DD; color:#556B2F;")
            self.setStyleSheet("background-color:#D4F4DD; color:#556B2F;")
            """self.setStyleSheet('''
                               #'''+self.name+''' {
                                 border: 2px solid white;
                                 border-radius: 5px;
                                 background-color: #D4F4DD;
                               }
                             ''')"""
    
    def build(self):
        #self.panels[i] = plantPanel
        panelLayout = QVBoxLayout()
        panelLayout.setContentsMargins(0, 0, 0, 0)
        panelLayout.setSpacing(0)
        panelLayout.setAlignment(Qt.AlignCenter)
        #print(panelLayout.getContentsMargins())
        self.setFixedWidth(300)
        self.setStyleSheet('''
                            QWidget {
                                background-color:none;
                                color:#556B2F;
                            }
                            
                            ''')
        
        # Name panel: Contains name and alias info
        namePanel = QWidget(self)
        nameLayout = QVBoxLayout()
        nameLayout.setContentsMargins(0, 0, 0, 0)
        nameLayout.setSpacing(0)
        nameLayout.setAlignment(Qt.AlignTop)
        namePanel.setFixedHeight(90)
        self.nameLabel = QLabel(f"{self.count}x {self.name}", namePanel)
        self.nameLabel.setFixedHeight(60)
        self.nameLabel.setAlignment(Qt.AlignBottom | Qt.AlignCenter)
        self.nameLabel.setFont(QFont('Garamond', 16, QFont.Bold))
        nameLayout.addWidget(self.nameLabel)
        #print(1)
        #aliasLabel = QLabel(f"(Alias: {self.alias})", namePanel)
        #aliasLabel.setFixedHeight(30)
        #aliasLabel.setFont(QFont('Garamond', 12, QFont.Bold))
        #aliasLabel.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        #nameLayout.addWidget(aliasLabel)
        #print(2)
        namePanel.setLayout(nameLayout)
        panelLayout.addWidget(namePanel)
        #print(3)
        # Gallery panel: Contains image of plant and button to show more images
        galleryPanel = QWidget(self)
        galleryLayout = QVBoxLayout()
        galleryLayout.setContentsMargins(0, 0, 0, 0)
        galleryLayout.setSpacing(0)
        galleryLayout.setAlignment(Qt.AlignTop)
        galleryPanel.setFixedHeight(270)
        galleryPanel.setLayout(galleryLayout)
        #print(4)
        mainPlantImage = QLabel(galleryPanel)
        #print(5)
        #print(self.image)
        imagePixmap = QPixmap(self.image)
        #print(6)
        mainPlantImage.setPixmap(imagePixmap)
        #print(7)
        mainPlantImage.setFixedHeight(200)
        mainPlantImage.setFixedWidth(300)
        #print(8)
        mainPlantImage.setScaledContents(True)
        #print(9)
        galleryLayout.addWidget(mainPlantImage)
        #print(10)
        gallerySeeMoreOption = QWidget(galleryPanel)
        gallerySeeMoreLayout = QHBoxLayout()
        gallerySeeMoreLayout.setContentsMargins(0, 0, 0, 0)
        gallerySeeMoreLayout.setSpacing(0)
        gallerySeeMoreOption.setFixedHeight(70)
        
        generalPlantImage = QLabel(gallerySeeMoreOption)
        generalPlantImage.setPixmap(imagePixmap) # TODO Set to same as main plant - change to be the default picture
        generalPlantImage.setFixedWidth(40)
        generalPlantImage.setFixedHeight(40)
        generalPlantImage.setScaledContents(True)
        gallerySeeMoreLayout.addWidget(generalPlantImage)
        galleryButton = QPushButton('Show Gallery', gallerySeeMoreOption)
        galleryButton.setFixedWidth(140)
        galleryButton.setFixedHeight(40)
        galleryButton.setStyleSheet('''
                                    QPushButton {
        background-color:#B0B0B0;  /* yellow background */
        color: white;               /* White text */
        border: 2px solid #9C9C9C;  /* Darker yellow border */
        border-radius: 12px;        /* Rounded corners */
        padding: 10px 24px;         /* Padding inside the button */
        font-size: 14px;            /* Font size */
    }
    QPushButton:hover {
        background-color: #9C9C9C;  /* Darker yellow when hovered */
        border: 2px solid #808080;  /* Darker border when hovered */
    }
    QPushButton:pressed {
        background-color:#808080;  /* Even darker yellow when pressed */
        border: 2px solid#6A6A6A;  /* Darker border when pressed */
    }
                                    ''')
        
        gallerySeeMoreLayout.addWidget(galleryButton)
        gallerySeeMoreOption.setLayout(gallerySeeMoreLayout)
        galleryLayout.addWidget(gallerySeeMoreOption)
        galleryPanel.setLayout(galleryLayout)
        
        panelLayout.addWidget(galleryPanel)
        
        # Property panel: Contains general property info of each plant
        propertyPanel = QWidget(self)
        propertyLayout = QVBoxLayout()
        propertyLayout.setContentsMargins(0, 0, 0, 0)
        propertyLayout.setSpacing(0)
        propertyLayout.setAlignment(Qt.AlignCenter)
        propertyPanel.setFixedHeight(50)
        #print("steve")
        sizeLabel = QLabel(f"Size: {self.plantSize} m", propertyPanel)
        sizeLabel.setFixedHeight(25)
        sizeLabel.setAlignment(Qt.AlignCenter)
        sizeLabel.setFont(QFont('Garamond', 12, QFont.Bold))
        propertyLayout.addWidget(sizeLabel)
        
        environmentLabel = QLabel(f"Environment: {self.environment}", propertyPanel)
        environmentLabel.setFixedHeight(25)
        environmentLabel.setFont(QFont('Garamond', 12, QFont.Bold))
        #environmentLabel.setAlignment(Qt.AlignCenter)
        propertyLayout.addWidget(environmentLabel)
        
        propertyPanel.setLayout(propertyLayout)
        panelLayout.addWidget(propertyPanel)
        
        # Select Button - MUST BE BLUE
        selectPanel = QWidget(self)
        selectLayout = QHBoxLayout()
        selectLayout.setContentsMargins(0, 0, 0, 0)
        selectLayout.setSpacing(0)
        selectLayout.setAlignment(Qt.AlignCenter)
        selectPanel.setFixedHeight(70)
        #print("Waffle")
        self.selectButton = QPushButton("+1", selectPanel) # need to track?
        self.deselectButton = QPushButton("-1", selectPanel)
        self.countLabel = QLabel("0", selectPanel)
        self.countLabel.setFixedWidth(50)
        self.countLabel.setStyleSheet("font-size: 24px;")
        self.countLabel.setAlignment(Qt.AlignCenter)
        #self.buttons[i] = selectButton
        self.selectButton.setFixedHeight(50)
        self.selectButton.setFixedWidth(50)
        self.deselectButton.setFixedHeight(50)
        self.deselectButton.setFixedWidth(50)
        self.selectButton.setStyleSheet(
        '''
            QPushButton {
                background-color: #008CBA;  /* Blue background */
                color: white;               /* White text */
                border: 2px solid #007B9A;  /* Darker blue border */
                border-radius: 12px;        /* Rounded corners */
                padding: 5px 12px;         /* Padding inside the button */
                font-size: 16px;            /* Font size */
            }
            QPushButton:hover {
                background-color: #007B9A;  /* Darker blue when hovered */
                border: 2px solid #005F73;  /* Darker border when hovered */
            }
            QPushButton:pressed {
                background-color: #005F73;  /* Even darker blue when pressed */
                border: 2px solid #004E5A;  /* Darker border when pressed */
            }
        '''
            
        )
        
        self.deselectButton.setStyleSheet(
        '''
            QPushButton {
                background-color: #008CBA;  /* Blue background */
                color: white;               /* White text */
                border: 2px solid #007B9A;  /* Darker blue border */
                border-radius: 12px;        /* Rounded corners */
                padding: 5px 12px;         /* Padding inside the button */
                font-size: 16px;            /* Font size */
            }
            QPushButton:hover {
                background-color: #007B9A;  /* Darker blue when hovered */
                border: 2px solid #005F73;  /* Darker border when hovered */
            }
            QPushButton:pressed {
                background-color: #005F73;  /* Even darker blue when pressed */
                border: 2px solid #004E5A;  /* Darker border when pressed */
            }
        '''
            
        )
        #print(1)
        self.selectButton.clicked.connect(self.plantIncrement)
        self.deselectButton.clicked.connect(self.plantDecrement)
        #print(3)
        #selectButton.setAlignment(Qt.AlignCenter)
        selectLayout.addWidget(self.deselectButton)
        selectLayout.addWidget(self.countLabel)
        selectLayout.addWidget(self.selectButton)
        selectPanel.setLayout(selectLayout)
        
        panelLayout.addWidget(selectPanel)
        
        self.setLayout(panelLayout)
        
#Third pop up window
#output
class output_window(QWidget):
    
    collection_count = 0
    collection_limit = 0
    
    care_to_show = []
    listOfPlants = []
    
    length_to_show = []
    name_selected = []
    
    def __init__(self, environment, garden_size, parent=None):
        super().__init__(parent)
        
        self.environment = environment
        self.garden_size = garden_size

        #????????????????????????????????????????????????????????????????????????????????????????????????????
        #call c# file to do process
        list = subprocess.run(["dotnet", "run", "--", environment, garden_size], capture_output=True, text=True)
        #can be this 
        
        #list = subprocess.run(["dotnet", "exec", "bin/Debug/net9.0/SE_backend.dll", environment, garden_size], capture_output=True, text=True)
        
        #parse list from c# file
        #print(list.stdout)
        
        name_length_care_image_list = list.stdout[1:-2].split("name:")
        #print(name_length_care_image_list)
        #print("\n\n\n\n\n")
        #print(name_length_care_image_list[1])
        #name_length_care_image_list.pop()
        #print(name_care_list)
        
        name_list =   []
        length_list = []
        care_list =   []
        image_list =  []        

        for entry in name_length_care_image_list:
            
            length_index = entry.find("length:")
            care_index = entry.find("care:")
            image_index = entry.find("image:")
            
            names = entry[:length_index].strip().split(", ")
            lengths = [x.strip() for x in entry[length_index + len("length:"):care_index].strip().split(",")]
            care = entry[care_index + len("care:"):image_index].strip()
            images = entry[image_index + len("image:"):].strip().split(", ")
            
            name_list.append(names)
            length_list.append(lengths)
            care_list.append(care)
            image_list.append(images)
        
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #will need to worry about length section here as well
        #print(name_list)    
        name_list.pop(0)
        length_list.pop(0)
        care_list.pop(0)
        image_list.pop(0)
        
        #when using this later just want first 5 entries
        #print(name_list)#name list will be 5 names at index 0, 5 names at index 1 and so on
        #print("\n")
        #print(length_list)
        #print("\n")
        #print(image_list)
        #print(care_list)#care list will be sunlight, water, design tip
        #print("\n")
        #print(image_list)
        #print("\n")
        #print(name_list[0])
        #names_to_show = name_list[0]
        #print(names_to_show[0]) #this works for first index use this
        
        #parse garden size 
        garden_sizes_lowercase = garden_size.lower()
        sizes = garden_sizes_lowercase.split('x')
        length = sizes[0]
        double_length = float(length)
        plant_panel.gardenSizeRemaining = double_length
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #integrating code here
        
        output_window.collection_limit = len(name_list) - 1
        
        if(output_window.collection_count > output_window.collection_limit):
            output_window.collection_count = 0
        
        names_to_show = name_list[self.collection_count]
        output_window.length_to_show = length_list[self.collection_count]
        #just send care no need to show here its next window
        output_window.care_to_show = care_list[self.collection_count]
        images_to_show = image_list[self.collection_count]
        double_length_to_show_0 = float(output_window.length_to_show[0])
        double_length_to_show_1 = float(output_window.length_to_show[1])
        double_length_to_show_2 = float(output_window.length_to_show[2])
        double_length_to_show_3 = float(output_window.length_to_show[3])
        double_length_to_show_4 = float(output_window.length_to_show[4])
        
        output_window.name_selected = names_to_show
        
        #all fields will always have 5 values make sure xml is structured accordingly
        plants = [
            [names_to_show[0], names_to_show[1], names_to_show[2], names_to_show[3], names_to_show[4]],#name
            ["delete", "delete", "delete", "delete", "delete"], # altname
            [environment, environment, environment, environment, environment], # environment
            [images_to_show[0], images_to_show[1], images_to_show[2], images_to_show[3], images_to_show[4]],
            [double_length_to_show_0, double_length_to_show_1, double_length_to_show_2, double_length_to_show_3, double_length_to_show_4], # size
            [0,              0,           0,             0,            0] # count
        ]

        #Window properties
        self.setWindowTitle('Recommendations')
        self.setFixedSize(1500, 700)

        self.setStyleSheet('''
                           QWidget {
                               background-color:#CDE0C9;
                           }
                           ''')

        #Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        #double_garden_size_remaining = round(plant_panel.gardenSizeRemaining, 2)

        plant_panel.header = QLabel(f"Here are the plants we've selected -- Room Remaining: {round(plant_panel.gardenSizeRemaining, 2)}", self)
        plant_panel.header.setFont(QFont('Garamond', 24, QFont.Bold))
        plant_panel.header.setFixedHeight(100)
        plant_panel.header.setAlignment(Qt.AlignCenter)
        plant_panel.header.setStyleSheet('''
                             QLabel {
                                 background-color:#D4F4DD;
                                 color:#556B2F;
                             }
                             
                             ''')
        
        layout.addWidget(plant_panel.header)

        #Add labels to display the environment and garden size
        #layout.addWidget(QLabel(f"Environment: {environment}", self))
        #layout.addWidget(QLabel(f"Garden Measurements: {garden_size}", self))

        NUM_PLANTS = 5
        
        plantList = QWidget(self)
        listLayout = QHBoxLayout(plantList)
        listLayout.setContentsMargins(0, 0, 0, 0)
        listLayout.setSpacing(0)
        plantList.setFixedHeight(480)
    
        output_window.listOfPlants = []
        
        for i in range(NUM_PLANTS):
            
            # Main panel - contains all plant info
            plantPanel = plant_panel(plantList, i, plants[0][i], plants[1][i], plants[3][i], plants[4][i], plants[2][i], plants[5][i])
            plantPanel.build()
            output_window.listOfPlants.insert(i, plantPanel)
            listLayout.addWidget(plantPanel)

        layout.addWidget(plantList)
        
        errorWidget = QWidget(self)
        errorLayout = QVBoxLayout()
        errorLayout.setContentsMargins(0, 0, 0, 0)
        errorLayout.setSpacing(0)
        errorWidget.setFixedHeight(20)
        
        plant_panel.errorMsg = QLabel(errorWidget)
        
        plant_panel.errorMsg.setFixedHeight(20)
        plant_panel.errorMsg.setStyleSheet("font-size: 16px; color: red;")
        plant_panel.errorMsg.setAlignment(Qt.AlignCenter)
        
        errorLayout.addWidget(plant_panel.errorMsg)
        errorWidget.setLayout(errorLayout)
        
        layout.addWidget(errorWidget)
        
        proceedOptions = QWidget(self)
        proceedOptionsLayout = QHBoxLayout()
        proceedOptionsLayout.setAlignment(Qt.AlignCenter)
        #proceedOptionsLayout.setContentsMargins(100, 0, 0, 0)
        proceedOptionsLayout.setSpacing(100)
        proceedOptions.setFixedHeight(100)
        
        redoButton = QPushButton("I don't like this selection", proceedOptions)
        redoButton.setFixedHeight(80)
        redoButton.setFixedWidth(600)
        redoButton.setStyleSheet('''
                                 QPushButton {
                background-color:#D9534F;  /* yellow background */
                color: white;               /* White text */
                border: 2px solid #C03A36;  /* Darker yellow border */
                border-radius: 12px;        /* Rounded corners */
                padding: 10px 24px;         /* Padding inside the button */
                font-size: 24px;            /* Font size */
            }
            QPushButton:hover {
                background-color: #C03A36;  /* Darker yellow when hovered */
                border: 2px solid #A02824;  /* Darker border when hovered */
            }
            QPushButton:pressed {
                background-color:#A02824;  /* Even darker yellow when pressed */
                border: 2px solid#801D1A;  /* Darker border when pressed */
            }
                                 ''')
        
        redoButton.clicked.connect(self.redo)
        
        proceedButton = QPushButton("Proceed to Care Guide", self)
        proceedButton.setFixedHeight(80)
        proceedButton.setFixedWidth(600)
        proceedButton.setStyleSheet('''
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
                                    
                                    ''')
        proceedButton.clicked.connect(self.care_guide_init)
        #nahButton.setAlignment(Qt.AlignCenter)
        proceedOptionsLayout.addWidget(redoButton)
        proceedOptionsLayout.addWidget(proceedButton)
        proceedOptions.setLayout(proceedOptionsLayout)
        layout.addWidget(proceedOptions)
        
        #Set layout for the main window
        self.setLayout(layout)
        
    def redo(self):
        output_window.collection_count += 1
        
        if(output_window.collection_count > output_window.collection_limit):
            output_window.collection_count = 0
        
        self.close()
        self.new_window = output_window(self.environment, self.garden_size)
        self.new_window.show()
        
    def care_guide_init(self):
        for i in range(5):
            if self.listOfPlants[i].count > 0:
                #self.close() this will close the window so I took it out -kp
                self.care_guide_window = care_guide_window()
                self.care_guide_window.show()
                return
        
        plant_panel.errorMsg.setText("You didn't select anything, please select a plant to continue")

    
class care_guide_window(QWidget):
    
    def __init__(self):# added output_window
        # supertype initialization
        super().__init__()
            
        # 1500x700, green background
        self.setFixedWidth(1500)
        self.setFixedHeight(700)
        self.setStyleSheet("background-color:#D4F4DD; color:#556B2F;")
        
        self.setWindowTitle('Care Guide') #kp added this
        
        # full page layout
        layout = QHBoxLayout()
        # no margins
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        imagePanel = QWidget(self)
        # 300x700
        imagePanel.setFixedWidth(300)
        imagePanel.setFixedHeight(700)
        
        # image panel layout
        imagePanelLayout = QVBoxLayout()
        # no margins
        imagePanelLayout.setContentsMargins(0, 0, 0, 0)
        imagePanelLayout.setSpacing(0)
        
        plantLabelPanel = QWidget(self)
        # 300x700
        plantLabelPanel.setFixedWidth(300)
        plantLabelPanel.setFixedHeight(700)
        
        # plant label panel layout
        plantLabelPanelLayout = QVBoxLayout()
        # no margins
        plantLabelPanelLayout.setContentsMargins(0, 0, 0, 0)
        plantLabelPanelLayout.setSpacing(0)
        
        # number of plants that were selected
        plantCount = 0
        plantIndices = []
        length_list = []
        name_list = []
        amount_plant = []
        
        # loop to determine number of plants selected
        for i in range(5):
            if output_window.listOfPlants[i].count > 0:
                plantCount += 1
                plantIndices.append(i)
                holder = float(output_window.length_to_show[i])#holds the lengths of the selected plants
                length_list.append(holder)
                name_list.append(output_window.name_selected[i])#holds the names of the selected plants

                
        #print(length_list)
        #print(name_list)     
                
        # loop to display plant information
        for i in plantIndices:
            # plant in list
            plant = output_window.listOfPlants[i]
            # add a label+img for it
            
            # image
            plantImg = QLabel(imagePanel)
            #if there is only 1 type of plant selected, the image will be 300x300 to keep it from being stretched
            if plantCount == 1:
                 plantImg.setFixedWidth(300)
                 plantImg.setFixedHeight(int(300))
            #the pictures will fill the height of 700 in equal parts     
            else:  
                plantImg.setFixedWidth(300)
                plantImg.setFixedHeight(int(700/plantCount))
            plantImg.setScaledContents(True)
            plantPixmap = QPixmap(plant.image)
            plantImg.setPixmap(plantPixmap)
            imagePanelLayout.addWidget(plantImg)
            
            # label
            plantLabel = QLabel(plantLabelPanel)
            plantLabel.setFont(QFont('Garamond', 24))
            plantLabel.setStyleSheet("font-size: 22px; color: Black;")
            plantLabel.setStyleSheet
            plantLabel.setText(f"<b>{plant.count}x</b> {plant.name}")
            plantLabel.setFixedWidth(300)
            plantLabel.setFixedHeight(int(700/plantCount))
            plantLabelPanelLayout.addWidget(plantLabel)
        
        
        #rightmost panel - space remaining, sun, water, care tip
        
        # wrapping widget for all remaining collection information
        collectionInfo = QWidget(self)
        collectionInfo.setFixedWidth(900)
        collectionInfo.setFixedHeight(700)
        collectionInfoLayout = QVBoxLayout()
        
        # no margins
        collectionInfoLayout.setContentsMargins(0, 0, 0, 0)
        collectionInfoLayout.setSpacing(0)
        
        # room remaining widget
        roomRemainingWidget = QWidget(collectionInfo)
        roomRemainingWidget.setFixedWidth(900)
        roomRemainingWidget.setFixedHeight(350)
        roomRemainingLayout = QVBoxLayout()
        roomRemainingLayout.setContentsMargins(0, 0, 0, 0)
        roomRemainingLayout.setSpacing(0)
        
        roomRemainingLabel = QLabel(roomRemainingWidget)
        roomRemainingLabel.setFixedWidth(900)
        roomRemainingLabel.setFixedHeight(350)
        roomRemainingLabel.setStyleSheet("font-size: 22px; color: Black;")
        roomRemainingLabel.setFont(QFont('Garamond', 24))
        
        #calculate the number of how many more of each selected plant would fit
        remainingRoomString = (f"<div style = 'text-align: center;'><b>Size Remaining:</b> You have {round(plant_panel.gardenSizeRemaining, 2)} meters remaining!</div><br><br>")
        #for loop through the selected plants, calculate the # of plants that could fit, and all that to the remainingRoomString
        for i in range(len(plantIndices)):
            amount_plant = plant_panel.gardenSizeRemaining / float(length_list[i])
            amount_plant = int(math.floor(amount_plant))
            remainingRoomString += (f"<div style='text-align: left;'>You can add <b>{round(amount_plant, 0)}</b> of <b>{name_list[i]}</b>.</div>")
        #output the remainingRoomString into the roomRemainingLabel part of the care guide
        remainingRoomString += ("<div style='text-align: left;'>Revist previous screen to revise selection if desired.</div>")
        roomRemainingLabel.setText(remainingRoomString)
        
        roomRemainingLayout.addWidget(roomRemainingLabel)
        collectionInfoLayout.addWidget(roomRemainingWidget)
            
        # care widget
        careWidget = QWidget(collectionInfo)
        careWidget.setFixedWidth(900)
        careWidget.setFixedHeight(350)
        careLayout = QVBoxLayout()
        careLayout.setContentsMargins(0, 0, 0, 0)
        careLayout.setSpacing(0)
        
        careLabel = QLabel(careWidget)
        careLabel.setFixedWidth(900)
        careLabel.setFixedHeight(350)
        careLabel.setWordWrap(True)
        careLabel.setStyleSheet("font-size: 22px; color: Black;")
        careLabel.setFont(QFont('Garamond'))

        # parse, separate, set label
        care = output_window.care_to_show.split(", ")
        sun = care[0]
        water = care[1]
        tip = ", ".join(care[2:])
        careLabel.setText(f"<div style='text-align: center;'><b>Care Information</b></div><br><br><b>Sun Requirement:</b> {sun}<br><br><b>Water Requirement:</b> {water}<br><br><b>Design Tip:</b> {tip}")
        
        careLayout.addWidget(careLabel)#, stretch=1)
        collectionInfoLayout.addWidget(careWidget)
        
        #adding boarder colors and setting layouts
        plantLabelPanel.setStyleSheet("border: 2px solid blue;")
        imagePanel.setStyleSheet("border: 2px solid blue;")
        collectionInfo.setStyleSheet("border: 2px solid blue;")
        
        plantLabelPanel.setLayout(plantLabelPanelLayout)
        imagePanel.setLayout(imagePanelLayout)
        collectionInfo.setLayout(collectionInfoLayout)
            
        layout.addWidget(plantLabelPanel)
        layout.addWidget(imagePanel)
        layout.addWidget(collectionInfo)

        self.setLayout(layout)


#Main
#lauch first_window method to start GUI procedure 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    splash_pix = QPixmap("logo.png")  
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())  
    splash.show()

    # Create the main window after 3 seconds
    def start_app():
        global ex
        ex = first_window()
        ex.show()
        splash.finish(ex)

    QTimer.singleShot(3000, start_app)
    sys.exit(app.exec_())
