from datetime import datetime, date

def fix_dates(data: dict) -> dict:
    """
    Converts all `datetime.date` objects in a dict to `datetime.datetime`
    for MongoDB compatibility.
    """
    for key, value in data.items():
        if isinstance(value, date):
            data[key] = datetime(value.year, value.month, value.day)
    return data
