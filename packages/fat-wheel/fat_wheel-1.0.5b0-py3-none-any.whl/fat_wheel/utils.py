from datetime import datetime
import os

CURRENT_DATE = datetime.now()
YEAR = CURRENT_DATE.year
MONTH = CURRENT_DATE.month
DAY = CURRENT_DATE.day


def now(date_format='%Y-%m-%d-%H-%M-%S'):
    return datetime.now().strftime(date_format)


def parent_dir(path):
    return os.path.dirname(path)


def joinpath(*args, **kwargs):
    return os.path.join(*args, **kwargs)
