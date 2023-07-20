import eel
from tkinter import Tk, filedialog as fd

@eel.expose
def upload_file():
    root = Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    file = fd.askopenfilename()
    print(file)

if __name__ == "__main__":
    eel.init('additional_files\\gui')
    eel.brw.set_path('chrome', '.\\additional_files\\brave\\brave.exe')
    eel.start('file_access.html', size=(320, 120))