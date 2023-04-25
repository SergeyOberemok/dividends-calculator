
import pytest
from ...helpers.numbers import parseFloat, parseInt, exchange

@pytest.fixture
def intNumbersAndExpectations() -> list:
    return [(2, 2), ("2", 2), ("hello", 0)]

def test_parseInt(intNumbersAndExpectations) -> None:
    for number, expect in intNumbersAndExpectations:
        assert parseInt(number) == expect

@pytest.fixture
def floatNumbersAndExpectations() -> list:
    return [(2, 2), (2.2, 2.2), ("2.2", 2.2), ("hello", 0)]

def test_parseFloat(floatNumbersAndExpectations) -> None:
    for number, expect in floatNumbersAndExpectations:
        assert parseFloat(number) == expect

def test_exchange() -> None:
    number = 1
    exchangeRate = 2

    assert exchange(number, exchangeRate) == number * exchangeRate