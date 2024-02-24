from typing import Callable, Iterable, SupportsIndex, overload

class ObservableList(list):
    #asignmets: = += *=
    def __init__(self, eventhandler:Callable[..., None], *args) -> None:
        self.__eventhandler = eventhandler
        super().__init__(*args)
    
    def __send_event(self):
        try:
            self.__eventhandler(self)
            return
        except:
            pass
        try:
            self.__eventhandler()
        except:
            params = self.__eventhandler.__code__.co_varnames[:self.__eventhandler.__code__.co_argcount]
            name = self.__eventhandler.__name__
            raise TypeError(f"Invalid parametercount for event function ({name}) (can only be 0 or 1 self is not included),parameters: {params}")
    
    def __iadd__(self, __x: Iterable):
        ret_val = super().__iadd__(__x)
        self.__send_event()
        return ret_val
    
    def __imul__(self, __n: SupportsIndex) :
        ret_val = super().__imul__(__n)
        self.__send_event()
        return ret_val
    
    def __delitem__(self, __i: SupportsIndex | slice) -> None:
        super().__delitem__(__i)
        self.__send_event()
    
    def __delattr__(self, __name: str) -> None:
        super().__delattr__(__name)
        self.__send_event()
    
    def __setitem__(self, *args) -> None:
        super().__setitem__(*args)
        self.__send_event()
    
    def append(self, __object) -> None:
        print(__object)
        super().append(__object)
        self.__send_event()

    def extend(self, __iterable: Iterable) -> None:
        super().extend(__iterable)
        self.__send_event()

    def pop(self, __index: SupportsIndex = ...):
        super().pop(__index)
        self.__send_event()

    def insert(self, __index: SupportsIndex, __object) -> None:
        super().insert(__index, __object)
        self.__send_event()

    def remove(self, __value) -> None:
        super().remove(__value)
        self.__send_event()

    def sort(self, *args) -> None:
        super().sort(*args)
        self.__send_event()

    def sort(self, *, key: None = ..., reverse: bool = ...) -> None:
        super().sort(key=key, reverse=reverse)
        self.__send_event()