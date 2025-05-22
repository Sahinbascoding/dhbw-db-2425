from datetime import datetime, date

def fix_dates(data: dict) -> dict:
    for key, value in data.items():
        if isinstance(value, date) and not isinstance(value, datetime):
            data[key] = datetime(value.year, value.month, value.day)
        elif isinstance(value, str):
            try:
                # Versuche gängige Formate zu parsen (optional)
                parsed = datetime.fromisoformat(value)
                data[key] = parsed
            except ValueError:
                pass  # kein Datumsformat
    return data
