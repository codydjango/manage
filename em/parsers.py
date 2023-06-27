import re
from dateutil import parser, tz
from datetime import datetime

def find_year(s):
    match = re.search(r'\b\d{4}\b', s)
    if match:
        return int(match.group(0))
    else:
        return None

def bump_year_if_date_in_past(date: datetime) -> datetime:
    # if the month is still upcoming this year, use the current year, which is the default
    # otherwise, update the parsed_date to next year

    now = datetime.now()
    upcoming_this_year = False
    if date.month > now.month:
        upcoming_this_year = True
    elif date.month == now.month:
        if date.day > now.day:
            upcoming_this_year = True

    if not upcoming_this_year:
        return date.replace(year=now.year + 1)

    return date

def parse_date(datestr: str):
    input_string = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', datestr)
    year_input = find_year(input_string)
    default_date = datetime(datetime.now().year, 1, 1, tzinfo=tz.tzlocal()) # use local timezone
    parsed_date = parser.parse(input_string, default=default_date, fuzzy=True)

    if not year_input:
        parsed_date = bump_year_if_date_in_past(parsed_date)

    return parsed_date