import logging
from urllib import parse

from voluptuous import All, Length, Range, Coerce, Schema, MultipleInvalid


logger = logging.getLogger(__name__)


def url_validator(url: str):
    parsed = parse.urlparse(url)

    if not parsed.scheme or parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("invalid URL")

    return url


HotelSchema = Schema({
    'name': All(str, Length(min=1, max=64)),
    'address': All(str, Length(min=1, max=128)),
    'stars': All(Coerce(int), Range(min=0, max=5)),
    'contact': All(str, Length(min=1, max=128)),
    'phone': All(str, Length(min=1, max=32)),
    'uri': All(url_validator, Length(min=1, max=1024)),
})


def hotel_validator(row):
    """
    Return either valid row or None
    """

    try:
        return HotelSchema(row)
    except MultipleInvalid as exc:
        logger.warning("Invalid row %s: %s", row, exc)
