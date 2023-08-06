from core.number.BigFloat import BigFloat
from coreutility.date.NanoTimestamp import NanoTimestamp
from influxdb_client import Point


def build_point(measurement, instrument, price: BigFloat, nano_timestamp=None) -> Point:
    point = Point(measurement).tag("instrument", instrument).field("price", str(price))
    if nano_timestamp is None:
        point.time(NanoTimestamp.get_nanoseconds())
    else:
        point.time(nano_timestamp)
    return point

