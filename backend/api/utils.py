from django.db.models import F
from django.db.models.functions import ATan2, Cos, Power, Radians, Sin, Sqrt


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
