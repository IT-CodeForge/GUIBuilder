import eel
from tkinter import Tk, filedialog as fd

@eel.expose
def funct():
    pass

if __name__ == "__main__":
    eel.init('additional_files\\gui')
    eel.brw.set_path('chrome', 'C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe') #NOTE
    eel.start('main.html', size=(320, 120))