import datetime


def convert_to_week_num(date: str, format: str = "%Y-%m-%d", week_flag: str = "%V"):
    return datetime.datetime.strptime(date, format).strftime(week_flag)
