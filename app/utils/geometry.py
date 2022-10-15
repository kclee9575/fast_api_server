import utm

from shapely import wkb
from geoalchemy2.elements import WKBElement
from typing import Union
from pydantic import BaseModel

ARRIVE_DISTANCE = 15


class AbstractPosition(BaseModel):
    latitude: float
    longitude: float


def parse_point_to_xy(point: Union[WKBElement, str]):
    x, y = 0.0, 0.0

    try:
        if type(point) == str:
            # POINT({x}, {y}) 형태의 String 파싱 -> 그외는 에러
            point = point.replace("POINT", "").split(" ")

            # point 스트링 변환 후 리스트 -->  ['(37.4021', '127.1086)']
            x, y = float(point[0][1:]), float(point[1][:-1])

        else:
            wkb_data = wkb.loads(bytes(point))
            x, y = wkb_data.x, wkb_data.y

    except:
        pass

    return x, y


def lat_long_to_point_string(latitude: float, longitude: float):
    return f"POINT({latitude} {longitude})"


def parse_point_to_lat_long(point: Union[WKBElement, str]):
    result = None
    try:
        if type(point) == str:
            point = point.replace("POINT", "").split(" ")
            result = AbstractPosition(
                latitude=float(point[0][1:]), longitude=float(point[1][:-1])
            )
        else:
            wkb_data = wkb.loads(bytes(point))
            result = AbstractPosition(latitude=wkb_data.x, longitude=wkb_data.y)
    except:
        pass

    return result


def calculate_distance(start: AbstractPosition, end: AbstractPosition):
    try:
        utm_position_1 = utm.from_latlon(start.latitude, start.longitude)
        utm_position_2 = utm.from_latlon(end.latitude, end.longitude)
        if (
            utm_position_1[2] != utm_position_2[2]
            or utm_position_1[3] != utm_position_2[3]
        ):
            return float("inf")
        return (
            (utm_position_1[0] - utm_position_2[0]) ** 2
            + (utm_position_1[1] - utm_position_2[1]) ** 2
        ) ** 0.5
    except Exception:
        return float("inf")


def is_robot_arrived(robot: AbstractPosition, destination: AbstractPosition):
    if (
        robot.latitude == 0
        or robot.longitude == 0
        or destination.latitude == 0
        or destination.longitude == 0
    ):
        return False

    return calculate_distance(robot, destination) <= ARRIVE_DISTANCE
