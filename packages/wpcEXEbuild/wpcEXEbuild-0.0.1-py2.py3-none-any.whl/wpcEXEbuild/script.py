import sys
import PyInstaller.__main__
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
  
    return os.path.join(base_path, relative_path)

def generateEXE(file_name):
    PyInstaller.__main__.run([
    f'{file_name}',
    '-F',
    '--hidden-import=asyncio',
    '--hidden-import=numpy',
    '--hidden-import=usb', 
    f'--add-data={resource_path("Material")}/.;Material',  
])

def main():
    if len(sys.argv) < 2:
        print('Missing argument, You should add a python file name after "wpcEXEbuild" command.')
        sys.exit()
    file_name = sys.argv[1]
    if file_name[-3:] == '.py':
        generateEXE(file_name)
    else:
        print("It is not a legal .py file name.")
