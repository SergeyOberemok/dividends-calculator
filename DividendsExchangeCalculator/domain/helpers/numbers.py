
def parseFloat(value) -> float:
    if isinstance(value, float) or isinstance(value, int):
        return value
    if isinstance(value, str) and value.lstrip("+-").replace(".", "").isnumeric():
        return float(value)

    return 0


def parseInt(value) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str) and value.isnumeric():
        return int(value)

    return 0


def exchange(value: float, rate: float) -> float:
    return round(value * rate, 2)
