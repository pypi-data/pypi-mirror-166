'''
Module that defines different classes used to define view for MARBLE GUI
'''
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QLabel, QPushButton,
                             QGridLayout, QComboBox, QLineEdit,
                             QRadioButton, QCheckBox,
                             QHBoxLayout, QWidget, QSpinBox,
                            )
from PyQt5.QtGui import QIcon
from .utils import createStyleSheet, COLOR_KEYS, PROBABILITY_MAP
from .comms import Communicate

class UISection:
  '''
  Class that handles data sections identified
  from the user loaded file, via the backend run
  '''
  def __init__(self, props):
    self.idx = props["id"]
    self.secKey = props["secKey"]

    self.key = props["data"].key
    self.unit = props["data"].unit
    self.prob = props["data"].prob
    self.link = props["data"].link
    self.dType = props["data"].dType
    self.value = props["data"].value
    self.length = props["data"].length
    self.dClass = props["data"].dClass
    self.imp = props["data"].important
    self.count = props["data"].count
    self.shape = props["data"].shape
    self.entropy = props["data"].entropy
    self.updatedStart = self.secKey

    self.communicate = props["view"]


  def flagImportant(self):
    '''
    UI method that creates a checkbox for user to flag a section as important
    '''
    importantCheck = QCheckBox("Important")
    importantCheck.setChecked(self.imp)
    importantCheck.stateChanged.connect(lambda: self.handleValueChange(importantCheck.isChecked(), "important"))
    return importantCheck

  def createEditButton(self, editForm):
    '''
    UI method that creates the edit button for each section
    '''
    editIcon = QIcon("marble/frontend/static/images/show_more_less.png")
    editButton = QPushButton(editIcon, '')
    editButton.clicked.connect(lambda: handleEdit(editForm))

    def handleEdit(editForm):
      '''
      Handler function that allows section to expand/contract
      to allow editing of non-prominent section data
      '''
      editForm.setVisible(not editForm.isVisible())

    return editButton

  def createEditForm(self):
    '''
    UI method to create an extended form for user to update general section data
    '''
    def captureNewStart(value):
      '''
      Function that captures user provided start value
      '''
      self.updatedStart = value

    def sectionSaveButton(layout):
      saveIcon = QIcon("marble/frontend/static/images/save_sec.jpg")
      saveButton = QPushButton(saveIcon, "Save")
      saveButton.clicked.connect(lambda: self.handleSectionUpdate())
      layout.addWidget(saveButton)

    def inputFor(data, key, title, layout, dtype=None, placeholder=None):
      '''
      UI Function to create custom textfield component
      '''
      inputLabel = QLabel(f"&{title}:  ")
      # TODO the check to differentiate between numeric and non-numeric values is high risk
      # went this way because some start values are of type numpy.int64.
      # need  to clarify why and get this fixed - both logic and implementation

      if type(data) is int:
        inputField = QSpinBox()
        inputField.setMaximum(100000)
        inputField.setValue(data)
        if key == 'start':
          if dtype == 'f':
            inputField.setSingleStep(4)
          elif dtype == 'd':
            inputField.setSingleStep(8)
          inputField.valueChanged[int].connect(lambda: captureNewStart(inputField.value()))
      else:
        inputField = QLineEdit()
        inputField.setPlaceholderText(placeholder)
        inputField.setText(data)

      inputField.textChanged.connect(lambda: self.handleValueChange(inputField.text(), key))
      inputLabel.setBuddy(inputField)
      layout.addWidget(inputLabel)
      layout.addWidget(inputField)

    form = QWidget()
    formLayout = QHBoxLayout()

    inputFor(int(self.secKey), "start", "Start", formLayout, dtype=self.dType)
    inputFor(int(self.length), "length", "Length", formLayout, dtype=self.dType)
    inputFor(self.dType, "dType", "Data type", formLayout, placeholder="Enter data type")
    inputFor(self.link, "link", "Link", formLayout, placeholder="Enter link")
    inputFor(self.dClass, "dClass", "Data class", formLayout, placeholder="Enter length")
    sectionSaveButton(formLayout)

    form.setLayout(formLayout)
    return form

  def showCertainty(self):
    '''
    UI method that creates a component for user to indicate the certainity of thier input
    '''
    certaintyBox = QWidget()
    certaintyLayout = QHBoxLayout()

    certaintyLabel = QLabel("Input certainty: ")
    radioRed = QRadioButton()
    radioRed.setStyleSheet(createStyleSheet(element='radio', props={"color": COLOR_KEYS["RED"]}))
    if int(self.prob) <= PROBABILITY_MAP[COLOR_KEYS["RED"]]:
      radioRed.setChecked(True)
    radioRed.toggled.connect(lambda: signalProbChange(self, COLOR_KEYS["RED"]))

    radioYellow = QRadioButton()
    radioYellow.setStyleSheet(createStyleSheet(element='radio', props={"color": COLOR_KEYS["YELLOW"]}))
    if int(self.prob) > PROBABILITY_MAP[COLOR_KEYS["RED"]] and int(self.prob) < PROBABILITY_MAP[COLOR_KEYS["GREEN"]]:
      radioYellow.setChecked(True)
    radioYellow.toggled.connect(lambda: signalProbChange(self, COLOR_KEYS["YELLOW"]))

    radioGreen = QRadioButton()
    radioGreen.setStyleSheet(createStyleSheet(element='radio', props={"color": COLOR_KEYS["GREEN"]}))
    if int(self.prob) >= PROBABILITY_MAP[COLOR_KEYS["GREEN"]]:
      radioGreen.setChecked(True)
    radioGreen.toggled.connect(lambda: signalProbChange(self, COLOR_KEYS["GREEN"]))

    certaintyLayout.addWidget(certaintyLabel)
    certaintyLayout.addWidget(radioRed)
    certaintyLayout.addWidget(radioYellow)
    certaintyLayout.addWidget(radioGreen)
    certaintyBox.setLayout(certaintyLayout)

    def signalProbChange(self, flag):
      '''
      Handler function used to communicate users certainty info
      '''
      self.communicateWithSec.certainSignal[int].emit(PROBABILITY_MAP[flag])

    return certaintyBox

  def handleValueChange(self, newValue, key="prob"):
    '''
    Functional method to handle value change of input fields
    TODO can implementation of this calculation be improved?
    '''
    if key in ("length", "prob"):
      self.communicate.updateIntValue.emit(self.secKey, key, int(newValue))
    elif isinstance(newValue, bool):
      self.communicate.updateBoolValue.emit(self.secKey, key, newValue)
    else:
      self.communicate.updateStrValue.emit(self.secKey, key, newValue)

  def handleSectionUpdate(self):
    '''
    Functional method to signal change in start value
    '''
    self.communicate.updateSection.emit(self.secKey, self.updatedStart)

class Unidentified(UISection):
  '''
  Sub-class of Section that handles sections of dType == 'b'
  i.e., information not identified by the backend.
  #1 | Unidentified | button->identify (different identify tools) | "edit"
  '''
  def __init__(self, props):
    super().__init__(props)
    self.algoDropdown = None

  def createWidget(self):
    '''
    UI Method to create a widget to handle unidentified sections of the processed file
    '''
    unidentifiedLayout = QGridLayout()

    algoLabel = QLabel("&Algorithm: ")
    self.algoDropdown = QComboBox()
    self.algoDropdown.addItems(["Algo option 01", "Algo option 02", "Algo option 03", "Algo option 04"])
    algoLabel.setBuddy(self.algoDropdown)
    unidentifiedLayout.addWidget(algoLabel, 1, 0, Qt.AlignmentFlag.AlignRight)
    unidentifiedLayout.addWidget(self.algoDropdown, 1, 1, Qt.AlignmentFlag.AlignLeft)
    identifyIcon = QIcon("marble/frontend/static/images/identify.jpg")
    identifyButton = QPushButton(identifyIcon, "Identify")
    identifyButton.clicked.connect(lambda: self.handleIdentify())
    unidentifiedLayout.addWidget(identifyButton, 1, 2, Qt.AlignmentFlag.AlignLeft)

    unidentifiedLayout.setColumnStretch(3, 1)

    flag = self.flagImportant()
    # TODO enable button when functionality is clear, and handle data capture
    flag.setDisabled(True)
    editForm = self.createEditForm()
    editForm.setVisible(False)
    unidentifiedLayout.addWidget(flag, 1, 4, Qt.AlignmentFlag.AlignCenter)
    unidentifiedLayout.addWidget(self.createEditButton(editForm), 1, 5, Qt.AlignmentFlag.AlignCenter)
    unidentifiedLayout.addWidget(editForm, 2, 0, 1, 5, Qt. AlignmentFlag.AlignLeft)

    return unidentifiedLayout

  def handleIdentify(self):
    '''
    Handler method to communicate users request to identify the section with a specified algo
    TODO implement this and write doc string
    '''
    print(f'Processing Identify. Method selected: {self.algoDropdown.currentText()}')

class TextMetaData(UISection):
  '''
  Sub-class of Section that handles sections of dType == 'c'
  i.e., Textual metadata in the loaded file that was identified by the backend.
  '''
  def __init__(self, props):
    super().__init__(props)
    self.editForm = None
    self.communicateWithSec = Communicate()
    self.communicateWithSec.certainSignal[int].connect(self.handleValueChange)

  def createWidget(self):
    '''
    UI method to create a widget to handle textual metadata
    '''
    textMetadataLayout = QGridLayout()

    keyLabel = QLabel("&Key:  ")
    keyInput = QLineEdit()
    keyInput.textChanged.connect(lambda: self.handleValueChange(keyInput.text(), "key"))
    keyInput.setPlaceholderText('Enter key for value')
    keyInput.setText(self.key)
    keyLabel.setBuddy(keyInput)
    textMetadataLayout.addWidget(keyLabel, 1, 0, Qt.AlignmentFlag.AlignRight)
    textMetadataLayout.addWidget(keyInput, 1, 1, Qt.AlignmentFlag.AlignLeft)

    valueLabel = QLabel("&Value: ")
    sectionValue = QLabel(self.value)
    valueLabel.setBuddy(sectionValue)
    textMetadataLayout.addWidget(valueLabel, 1, 2, Qt.AlignmentFlag.AlignRight)
    textMetadataLayout.addWidget(sectionValue, 1, 3, Qt.AlignmentFlag.AlignLeft)

    textMetadataLayout.setColumnStretch(4, 1)

    certainty = self.showCertainty()
    textMetadataLayout.addWidget(certainty, 1, 5, 1, 1, Qt.AlignmentFlag.AlignHCenter)

    flag = self.flagImportant()
    editForm = self.createEditForm()
    editForm.setVisible(False)
    textMetadataLayout.addWidget(flag, 1, 6, Qt.AlignmentFlag.AlignCenter)
    textMetadataLayout.addWidget(self.createEditButton(editForm), 1, 7, Qt.AlignmentFlag.AlignCenter)
    textMetadataLayout.addWidget(editForm, 2, 0, 1, 6, Qt. AlignmentFlag.AlignLeft)

    return textMetadataLayout

class PrimaryData(UISection):
  '''
  Sub-class of Section that handles sections of dType == 'd' || dType=='f'
  i.e., information not identified by the backend
  '''
  def __init__(self, props):
    super().__init__(props)
    self.editForm = None
    self.communicateWithSec = Communicate()
    self.communicateWithSec.certainSignal[int].connect(self.handleValueChange)

  def createWidget(self):
    '''
    UI method to create a widget to handle primary/raw data
    '''
    primaryDataLayout = QGridLayout()

    keyLabel = QLabel("&Key:  ")
    keyInput = QLineEdit()
    keyInput.textChanged.connect(lambda: self.handleValueChange(keyInput.text(), "key"))
    keyInput.setPlaceholderText('Enter key for value')
    keyInput.setText(self.key)
    keyLabel.setBuddy(keyInput)
    primaryDataLayout.addWidget(keyLabel, 1, 0, Qt.AlignmentFlag.AlignRight)
    primaryDataLayout.addWidget(keyInput, 1, 1, Qt.AlignmentFlag.AlignLeft)

    unitLabel = QLabel("&Unit: ")
    unitInput = QLineEdit()
    unitInput.textChanged.connect(lambda: self.handleValueChange(unitInput.text(), "unit"))
    unitInput.setPlaceholderText('Enter unit for key')
    unitInput.setText(self.unit)
    unitLabel.setBuddy(unitInput)
    primaryDataLayout.addWidget(unitLabel, 1, 2, Qt.AlignmentFlag.AlignRight)
    primaryDataLayout.addWidget(unitInput, 1, 3, Qt.AlignmentFlag.AlignLeft)

    valueLabel = QLabel("&Value: ")
    sectionValue = QLabel(self.value)
    valueLabel.setBuddy(sectionValue)
    primaryDataLayout.addWidget(valueLabel, 1, 4, Qt.AlignmentFlag.AlignRight)
    primaryDataLayout.addWidget(sectionValue, 1, 5, Qt.AlignmentFlag.AlignLeft)

    drawIcon = QIcon("marble/frontend/static/images/draw.jpeg")
    drawButton = QPushButton(drawIcon, "Plot")
    drawButton.clicked.connect(lambda: self.handleDraw())
    primaryDataLayout.addWidget(drawButton, 1, 6, Qt.AlignmentFlag.AlignCenter)

    primaryDataLayout.setColumnStretch(7, 1)

    certainty = self.showCertainty()
    primaryDataLayout.addWidget(certainty, 1, 8, 1, 2, Qt.AlignmentFlag.AlignCenter)

    flag = self.flagImportant()
    editForm = self.createEditForm()
    editForm.setVisible(False)
    primaryDataLayout.addWidget(flag, 1, 10, 1, 1, Qt.AlignmentFlag.AlignVCenter)
    primaryDataLayout.addWidget(self.createEditButton(editForm), 1, 11, 1, 1, Qt.AlignmentFlag.AlignVCenter)
    primaryDataLayout.addWidget(editForm, 2, 0, 1, 10, Qt. AlignmentFlag.AlignLeft)

    return primaryDataLayout

  def handleDraw(self):
    '''
    Handler method that communicates users request to plot primary data of the section
    '''
    self.communicate.plotData[int].emit(self.secKey)
