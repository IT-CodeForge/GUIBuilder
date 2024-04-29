from intermediary_neu.intermediary import Intermediary
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IButton import IButton
from intermediary_neu.objects.ICanvas import ICanvas
from intermediary_neu.objects.ICheckbox import ICheckbox
from intermediary_neu.objects.IEdit import IEdit
from intermediary_neu.objects.ILabel import ILabel
from intermediary_neu.objects.ITimer import ITimer
from intermediary_neu.objects.IWindow import IWindow

if __name__ == "__main__":
    # Alles importierte wird einmal verwendet, damit keine "WirdNichtVerwendet" Warnung getriggert wird.
    Intermediary.create_object
    IBaseObject.id
    IButton.id
    ICanvas.id
    ICheckbox.id
    IEdit.id
    ILabel.id
    ITimer.id
    IWindow.id