import re
from math import radians, cos, sin, asin, sqrt

from django.db.models import F
from django.db.models.functions import ATan2, Cos, Power, Radians, Sin, Sqrt

PHONE_NUMBER_REGEX = re.compile(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?'
                                r'[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$')


def count_distance(cur_longitude, cur_latitude):
    current_lat = float(cur_latitude)
    current_long = float(cur_longitude)
    dlat = Radians(F('latitude') - current_lat)
    dlong = Radians(F('longitude') - current_long)

    a = (Power(Sin(dlat / 2), 2) + Cos(Radians(current_lat))
         * Cos(Radians(F('latitude'))) * Power(Sin(dlong / 2), 2)
         )

    c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))
    return 6371 * c


def haversine(lon1, lat1, lon2, lat2) -> float:
    """Возвращает расстояние в километрах между двумя точками планеты."""

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c


def dist_to_str(dist: float) -> str:
    """Возвращает форматированное расстояние."""

    if dist <= 1:
        return '~%0.2f м.' % (dist * 1000)
    if 1 < dist <= 10:
        return '~%.1f км' % dist
    return '> 10 км'
