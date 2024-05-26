from __future__ import annotations
from abc import abstractmethod
from typing import Any, Optional
from ..Vector2d import Vector2d
from .ETKBaseObject import ETKBaseObject


class ETKBaseWidget(ETKBaseObject):
    def __init__(self, *, pos: Vector2d, size: Vector2d, visibility: bool, background_color: int, **kwargs: Any) -> None:
        self._parent: Optional[ETKBaseWidget] = None
        self._enabled: bool = True

        super().__init__(pos=pos, size=size, visibility=visibility, background_color=background_color, **kwargs)

    # region Properties

    @ETKBaseObject.pos.setter
    def pos(self, value: Vector2d) -> None:
        ETKBaseObject.pos.fset(self, value)  # type:ignore
        if self.parent != None:
            self.parent._validate_pos(self)

        abspos = self.abs_pos
        if abspos.x < 0 or abspos.y < 0:
            raise RuntimeError(
                f"element {self} is outside of window\nelement: pos: {self.pos}")

        self._update_pos()

    @ETKBaseObject.size.setter
    def size(self, value: Vector2d) -> None:
        ETKBaseObject.size.fset(self, value)  # type:ignore
        if self.parent != None:
            self.parent._validate_size(self)

    @property
    def abs_pos(self) -> Vector2d:
        """READ-ONLY"""
        if self._parent != None:
            return self._parent._get_childs_abs_pos(self)
        return self.pos

    @property
    def parent(self) -> Optional[ETKBaseWidget]:
        return self._parent

    @ETKBaseObject.visibility.setter
    def visibility(self, value: bool) -> None:
        ETKBaseObject.visibility.fset(self, value)  # type:ignore
        self._update_visibility()
        if self._parent != None:
            self._parent._validate_visibility(self)

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

    @abstractmethod
    def _update_pos(self) -> None:
        pass

    @abstractmethod
    def _update_visibility(self) -> None:
        pass

    def _update_enabled(self) -> None:
        pass

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
