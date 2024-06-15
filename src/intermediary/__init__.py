from intermediary.Intermediary import Intermediary, IObjects, IObjectWidgets
from intermediary.objects.IBaseObject import IBaseObject
from intermediary.objects.IBaseObjectWidget import IBaseObjectWidget
from intermediary.objects.IBaseObjectWidgetText import IBaseObjectWidgetText
from intermediary.objects.IBaseObjectWidgetVisible import IBaseObjectWidgetVisible
from intermediary.objects.IBaseObjectWidgetVisibleEVChanged import IBaseObjectWidgetVisibleEVChanged
from intermediary.objects.IButton import IButton
from intermediary.objects.ICanvas import ICanvas
from intermediary.objects.ICheckbox import ICheckbox
from intermediary.objects.IEdit import IEdit
from intermediary.objects.ILabel import ILabel
from intermediary.objects.ITimer import ITimer
from intermediary.objects.IWindow import IWindow

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
    IBaseObjectWidget.ATTRIBUTES
    IBaseObjectWidgetText.ATTRIBUTES
    IBaseObjectWidgetVisible.ATTRIBUTES
    IBaseObjectWidgetVisibleEVChanged.ATTRIBUTES
    x: IObjects
    y: IObjectWidgets