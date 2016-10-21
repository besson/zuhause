from datetime import date

def parse_date(raw_date):
    if ("immediately" in raw_date):
        return date.today().isoformat()

    _date = raw_date.replace("from ", "").replace(".", "-")
    date_parts = _date.split(" ")[0].split("-")

    return "%s-%s-%s" % (date_parts[2], date_parts[1], date_parts[0])
