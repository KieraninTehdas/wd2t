from datetime import date, datetime


def get_utc_now() -> datetime:
    return datetime.utcnow()


def get_utc_today() -> date:
    return get_utc_now().date()
