'''
Module contains helper variables and functions for the MARBLE GUI application
'''
import time
from multiprocessing import Process
# The modules above are imported to create a setTimeout() [JS] like function in python
# to be used to imitate the proces of a backend call

# Defining a dictionary of variable name suffixes
VARIABLE_OPTIONS = {
  'BUTTON_ACTION': '_button_action',
  'MENU': '_menu',
}

# Defining Menu bar options and corresponding action options
MENU_TREE = {
  'File': ['New File', 'Open File', 'Save File', 'Revert File', 'Close File'],
  'Edit': ['Undo', 'Redo', 'Copy', 'Cut', 'Paste', 'Find', 'Replace'],
  'View': ['Open View', 'Appearance', 'Explorer', 'Problems', 'Testing', 'Word Wrap'],
  'Help': ['Get Started', 'Documentation', 'About']
}

# Color identifiers
COLOR_KEYS = {
  "RED": "_r",
  "YELLOW": "_y",
  "GREEN": "_g"
}

# Color profiles for UI
STYLESHEET_CONSTS = {
  "colors": {
    COLOR_KEYS["RED"]: "#d91309",
    COLOR_KEYS["YELLOW"]: "#f4f72a",
    COLOR_KEYS["GREEN"]: "#00ff0d"
  },
  "size": {
    "radio": 20,
  },
  "border": {
    "radio" : 2
  }
}

# Section Type
DTYPE_TO_SECTION_TITLE = {
  "b": "UNIDENTIFIED",
  "c": "TEXT METADATA",
  #"i": "TEXT METADATA(i)",
  "i": "TEXT METADATA",
  "d": "PRIMARY DATA",
  "f": "PRIMARY DATA",
  #"B": "PRIMARY DATA(B)",
  "B": "PRIMARY DATA"
}

# Color-probability map
PROBABILITY_MAP = {
  COLOR_KEYS["RED"]: 25,
  COLOR_KEYS["YELLOW"]: 50,
  COLOR_KEYS["GREEN"]: 75
}

# Creating an appropriate variable name
def createVariableNames(inputString, ext):
  '''
  Function to help create variables for different types of menu options/option buttons
  '''
  # converting string to lowercase
  lowerString = inputString.lower()
  # replacing all whitespaces with _, if input string contains more than one word
  prefix = lowerString.replace(' ', '_')
  return prefix+VARIABLE_OPTIONS[ext]

def createStyleSheet(element, props):
  '''
  Creates stylesheet for requested elements based on props given
  '''
  style = None
  if element == 'radio':
    colorCode = props["color"]
    radioSize = STYLESHEET_CONSTS["size"]["radio"]
    radioBorder = STYLESHEET_CONSTS["border"]["radio"]
    radioColor = STYLESHEET_CONSTS["colors"][colorCode]

    style = '''
    QRadioButton::indicator {{
      border: {border}px solid black;
      height: {size}px;
      width: {size}px;
      border-radius: {radius}px;
    }}
    QRadioButton::indicator:checked {{
      background: {color};
    }}
    '''.format(size=radioSize - radioBorder * 2,
               border=radioBorder,
               radius=radioSize//2,
               color=radioColor)
  return style

# Imitating the time break of backend call
# SOURCE - https://dreamix.eu/blog/webothers/timeout-function-in-python-3
def secondsPassed():
  '''
  Helper function that should timeout after 5 seconds.
  It simply prints a number and waits 1 second
  '''
  i = 0
  while True:
    i += 1
    print(i)
    time.sleep(1)


def setTimeOut():
  '''
  Each Process has its own memory space.
  Allows us to kill it without worrying that some resources are left open
  '''
  # Create a Process
  actionProcess = Process(target=secondsPassed)

  # Start the process and block it for 5 seconds.
  actionProcess.start()
  actionProcess.join(timeout=10)

  # Terminate the process
  actionProcess.terminate()
