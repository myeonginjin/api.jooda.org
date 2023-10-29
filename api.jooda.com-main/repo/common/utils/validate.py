from datetime import datetime
from re import match


def validate_date(
    year: str = None, month: str = None, day: str = None, date: str = None
) -> tuple:
    if date:
        if not match(r"^[0-9][0-9][0-9][0-9]", date):
            date = "20" + date
        date = datetime.strptime(date, "%Y-%m-%d")
    else:
        year, month, day = str(year), str(month), str(day)
        year = year if len(year) == 4 else "20" + year
        date = datetime.strptime(year + "-" + month + "-" + day, "%Y-%m-%d")
    year, month, day = str(date.year), str(date.month), str(date.day)
    return (
        year[2:4],
        month if len(month) == 2 else "0" + month,
        day if len(day) == 2 else "0" + day,
    )


def validate_start_end_date(start_date: str, end_date: str) -> tuple:
    start_year, start_month, start_day = validate_date(date=start_date)
    start_date = f"20{start_year}-{start_month}-{start_day}"
    if end_date:
        end_year, end_month, end_day = validate_date(date=end_date)
        end_date = f"20{end_year}-{end_month}-{end_day}"
        if start_date.__gt__(end_date):
            return None, None
        elif start_date.__eq__(end_date):
            end_date = None
    return start_date, end_date


def validate_time(start_time: str, end_time: str) -> tuple:
    start_time = datetime.strptime(start_time, "%H:%M")
    if end_time:
        end_time = datetime.strptime(end_time, "%H:%M")
        if start_time.__gt__(end_time):
            return None, None
        if start_time.__eq__(end_time):
            end_time = None
    return start_time, end_time
