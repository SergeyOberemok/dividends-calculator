
class Country:
    _code: str
    _name: str
    _isTaxRelief: bool

    def __init__(self, code: str, name: str = '', isTaxRelief: bool = False) -> None:
        self._code = code
        self._name = name
        self._isTaxRelief = isTaxRelief

    @property
    def name(self) -> str:
        return self._name

    @property
    def isTaxRelief(self) -> bool:
        return self._isTaxRelief

    def __str__(self) -> str:
        return self._code

    def __eq__(self, obj) -> bool:
        if isinstance(obj, Country):
            return str(self) == str(obj)
        if isinstance(obj, str):
            return self._code == obj
        return False


