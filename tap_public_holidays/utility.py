import os
from datetime import datetime
import requests


# constants
base_url = "https://publicholidays.co.nz"
base_format = "%Y-%m-%dT%H:%M:%S"


def get_data(year):
    return requests.get(f"{base_url}/{year}-dates/").text


def format_date(dt, format=base_format):
    return datetime.strftime(dt, format)


def parse_date(str, format=base_format):
    try:
        return datetime.strptime(str, format)
    except:
        if format == base_format:
            raise
        else:
            return datetime.strptime(str, base_format)


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)
