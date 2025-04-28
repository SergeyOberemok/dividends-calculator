
from datetime import datetime, timedelta


def parseDate(dateToParse: str, dateFormat: str) -> datetime:
    return datetime.strptime(dateToParse, dateFormat)


def parseISODate(dateToParse: str) -> datetime:
    return datetime.fromisoformat(dateToParse)


def substractDays(date: datetime, days: int) -> datetime:
    return date - timedelta(days=days)


def getDayBefore(date: datetime) -> datetime:
    return substractDays(date, 1)


def getWorkingDayBefore(date: datetime) -> datetime:
    if date.isoweekday() == 1:
        daysToSubstract = 3
    elif date.isoweekday() == 7:
        daysToSubstract = 2
    elif date.isoweekday() == 6:
        daysToSubstract = 1
    else:
        daysToSubstract = 1

    return substractDays(date, daysToSubstract)


def toDateStringISO(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")


def printDay(date: datetime) -> str:
    return date.strftime("%A")
