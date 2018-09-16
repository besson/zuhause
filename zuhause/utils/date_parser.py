from datetime import date
from datetime import datetime


def parse_date(raw_date):
    try:
        _date = raw_date.strip().replace("from ", "").replace(".", "-").replace("/", "-")
        date_parts = _date.split(" ")[0].split("-")

        formatted_date = "%s-%s-%s" % (date_parts[2], date_parts[1], date_parts[0])
        datetime.strptime(formatted_date, '%YYYY-%mm-%dd')

        return formatted_date
    except:
        return date.today().isoformat()
