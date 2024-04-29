"""Diese Datei hat alle vom Endnutzer benötigten Module von ETK importiert. Der Endnutzer kann diese von dieser Datei einzeln oder mit * alle existierenden importieren."""


from ETKV2.Internal.ETKBaseObject import ETKBaseEvents, ETKBaseObject
from ETKV2.Internal.ETKBaseWidget import ETKBaseWidget
from ETKV2.Internal.ETKBaseTkObject import ETKBaseTkObject
from ETKV2.Internal.ETKBaseTkWidget import ETKBaseTkWidget, ETKBaseWidget
from ETKV2.Internal.ETKBaseWidgetDisableable import ETKBaseWidgetDisableable
from ETKV2.Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from ETKV2.Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText
from ETKV2.ETKBitmap import ETKBitmap
from ETKV2.ETKButton import ETKButton, ETKButtonEvents
from ETKV2.ETKCanvas import ETKCanvas
from ETKV2.ETKCanvasCircle import ETKCanvasCircle
from ETKV2.ETKCanvasItem import ETKCanvasItem
from ETKV2.ETKCanvasLine import ETKCanvasLine
from ETKV2.ETKCanvasOval import ETKCanvasOval
from ETKV2.ETKCanvasRectangle import ETKCanvasRectangle
from ETKV2.ETKCanvasSquare import ETKCanvasSquare
from ETKV2.ETKCheckbox import ETKCheckbox, ETKCheckboxEvents
from ETKV2.Internal.ETKBaseContainer import ETKAlignments, ETKContainerSize, ETKBaseContainer
from ETKV2.ETKContainer import ETKContainer
from ETKV2.ETKEdit import ETKEdit, ETKEditEvents
from ETKV2.ETKLabel import ETKLabel
from ETKV2.ETKListingContainer import ETKListingContainer, ETKListingTypes
from ETKV2.ETKMainWindow import ETKMainWindow, ETKWindowEvents
from ETKV2.ETKTimer import ETKTimer
from ETKV2.vector2d import vector2d
from ETKV2.ETKDropdownMenu import ETKDropdownMenu, ETKDropdownMenuEvents


if __name__ == "__main__":
    # Alles importierte wird einmal verwendet, damit keine "WirdNichtVerwendet" Warnung getriggert wird.
    ETKBaseEvents.ENTER
    ETKBitmap.abs_enabled
    ETKButton.abs_enabled
    ETKButtonEvents.PRESSED
    ETKCanvas.abs_enabled
    ETKCanvasCircle.background_color
    ETKCanvasItem.background_color
    ETKCanvasLine.background_color
    ETKCanvasOval.background_color
    ETKCanvasRectangle.background_color
    ETKCanvasSquare.background_color
    ETKCheckbox.abs_enabled
    ETKCheckboxEvents.CHECKED
    ETKAlignments.BOTTOM_CENTER
    ETKContainerSize.copy
    ETKContainer.abs_enabled
    ETKEdit.abs_enabled
    ETKEditEvents.CHANGED
    ETKLabel.abs_enabled
    ETKListingContainer.abs_enabled
    ETKListingTypes.BOTTOM_TO_TOP
    ETKMainWindow.abs_pos
    ETKWindowEvents.EXIT
    ETKTimer.mro
    vector2d.mro
    ETKDropdownMenu.abs_enabled
    ETKDropdownMenuEvents.CHANGED
    ETKBaseContainer.abs_enabled
    ETKBaseObject.abs_pos
    ETKBaseWidget.abs_enabled
    ETKBaseTkObject.abs_pos
    ETKBaseTkWidget.abs_enabled
    ETKBaseWidgetDisableable.abs_enabled
    ETKBaseTkWidgetDisableable.abs_enabled
    ETKBaseTkWidgetText.abs_enabled
