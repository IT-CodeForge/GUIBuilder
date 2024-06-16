from ..exceptions import UserError

class ParsingError(UserError):
    def __init__(self, err_dt: str, err_en: str) -> None:
        super().__init__(err_dt, err_en)