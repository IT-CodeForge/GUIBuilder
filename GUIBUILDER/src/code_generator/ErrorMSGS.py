class UserError(Exception):
    def __init__(self, err_dt: str, err_en: str) -> None:
        self.err_dt = err_dt
        self.err_en = err_en
        super().__init__(self.err_en)

class ParsingError(UserError):
    def __init__(self, err_dt: str, err_en: str) -> None:
        super().__init__(err_dt, err_en)