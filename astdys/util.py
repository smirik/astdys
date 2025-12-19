import datetime


def convert_mjd_to_datetime(mjd: float) -> datetime.datetime:
    """Convert Modified Julian Date to datetime object.

    Args:
        mjd: Modified Julian Date value

    Returns:
        datetime object representing the date
    """
    base_date = datetime.datetime(1858, 11, 17)
    return base_date + datetime.timedelta(days=mjd)


def convert_mjd_to_date(mjd: float) -> str:
    """Convert Modified Julian Date to formatted string.

    Args:
        mjd: Modified Julian Date value

    Returns:
        Formatted date string (YYYY-MM-DD HH:MM:SS)
    """
    dt = convert_mjd_to_datetime(mjd)
    return dt.strftime("%Y-%m-%d %H:%M:%S")
