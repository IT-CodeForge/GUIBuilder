from intermediary_neu.Intermediary import Intermediary, IObjects, IObjectWidgets
from intermediary_neu.objects.IBaseObject import IBaseObject
from intermediary_neu.objects.IBaseObjectWidget import IBaseObjectWidget
from intermediary_neu.objects.IBaseObjectWidgetText import IBaseObjectWidgetText
from intermediary_neu.objects.IBaseObjectWidgetVisible import IBaseObjectWidgetVisible
from intermediary_neu.objects.IBaseObjectWidgetVisibleEVChanged import IBaseObjectWidgetVisibleEVChanged
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
    IBaseObjectWidget.ATTRIBUTES
    IBaseObjectWidgetText.ATTRIBUTES
    IBaseObjectWidgetVisible.ATTRIBUTES
    IBaseObjectWidgetVisibleEVChanged.ATTRIBUTES
    x: IObjects
    y: IObjectWidgets