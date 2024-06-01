from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional

from ..Vector2d import Vector2d
from .ETKBaseObject import ETKBaseObject

if TYPE_CHECKING:
    from ..ETKMainWindow import ETKMain


class ETKBaseWidget(ETKBaseObject):
    def __init__(self, *, main: ETKMain, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int, **kwargs: Any) -> None:
        self._parent: Optional[ETKBaseWidget] = None
        self._enabled: bool = True
        self.__akt_visibility: bool
        self.__akt_pos: Vector2d
        self.__akt_size: Vector2d
        self.__akt_enabled: bool

        super().__init__(main=main, pos=pos, size=size, visibility=visibility, background_color=background_color, **kwargs)

    # region Properties

    @property
    def abs_pos(self) -> Vector2d:
        """READ-ONLY"""
        if self._parent != None:
            return self._parent._get_childs_abs_pos(self)
        return self.pos

    @property
    def parent(self) -> Optional[ETKBaseWidget]:
        return self._parent

    @property
    def abs_visibility(self) -> bool:
        """READ-ONLY"""
        if self._parent != None:
            return self.visibility and self._parent.abs_visibility
        return self.visibility

    @property
    def enabled(self) -> bool:
        """READ-ONLY"""
        return self._enabled

    @property
    def abs_enabled(self) -> bool:
        """READ-ONLY"""
        if self._parent != None:
            return self._enabled and self._parent._enabled
        return self._enabled

    # endregion
    # region Methods

    def detach_from_parent(self) -> None:
        if self._parent is None:
            raise ValueError(f"{self} has no parent!")
        self._parent._detach_child(self)

    # region update event methods

    def _update_pos(self, validation: bool = True) -> bool:
        abspos = self.abs_pos
        if abspos == getattr(self, "__akt_pos", Vector2d() if abspos != Vector2d() else Vector2d(1)):
            return False

        if self.parent != None and validation:
            self.parent._validate_pos(self)

        if abspos.x < 0 or abspos.y < 0:
            raise RuntimeError(
                f"element {self} is outside of window\nelement: pos: {self.pos}")
        return True

    def _update_size(self, validation: bool = True) -> bool:
        try:  # NOTE
            size = self.size.vec  # type:ignore
        except:
            size = self.size
        akt_size_0 = getattr(self, "__akt_size", Vector2d() if size != Vector2d() else Vector2d(1))
        try:
            akt_size = akt_size_0.vec  # type:ignore
        except:
            akt_size = akt_size_0
        if size == akt_size:
            return False

        if self.parent != None and validation:
            self.parent._validate_size(self)
        return True

    def _update_visibility(self, validation: bool = True) -> bool:
        if self.abs_visibility == getattr(self, "__akt_visibility", not self.abs_visibility):
            return False

        if self._parent != None and validation:
            self._parent._validate_visibility(self)
        return True

    def _update_enabled(self) -> bool:
        if self.abs_enabled == getattr(self, "__akt_enabled", not self.abs_enabled):
            return False
        return True

    # endregion
    # region child validation methods

    def _get_childs_abs_pos(self, child: ETKBaseWidget) -> Vector2d:
        return self.abs_pos + child.pos

    def _detach_child(self, element: ETKBaseWidget) -> None:
        if element._parent != self:
            raise ValueError(f"{self} is not the parent of {element}!")
        element._parent = None

    def _validate_pos(self, element: ETKBaseWidget) -> None:
        pass

    def _validate_size(self, element: ETKBaseWidget) -> None:
        pass

    def _validate_visibility(self, element: ETKBaseWidget) -> None:
        pass

    # endregion
    # endregion
