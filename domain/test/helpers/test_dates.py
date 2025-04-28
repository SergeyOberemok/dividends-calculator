
from datetime import datetime
from ...helpers.dates import parseISODate, getWorkingDayBefore
import pytest


def test_parseISODate() -> None:
    result = parseISODate("2023-05-25")

    assert isinstance(result, datetime)
    assert result == datetime(2023, 5, 25)


@pytest.fixture
def workingDatesAndExpectations() -> list:
    return [
        (datetime(2023, 4, 26), datetime(2023, 4, 25)),
        (datetime(2023, 4, 24), datetime(2023, 4, 21)),
        (datetime(2023, 4, 23), datetime(2023, 4, 21)),
        (datetime(2023, 4, 22), datetime(2023, 4, 21)),
    ]


def test_getWorkingDayBefore(workingDatesAndExpectations) -> None:
    for date, expected in workingDatesAndExpectations:
        assert getWorkingDayBefore(date) == expected
