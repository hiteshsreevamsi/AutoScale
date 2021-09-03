import numpy as np


def reachable_zip_code(slat, slong, dlat, dlong, dist):
    R = 6373.0
    lat1 = np.radians(slat)
    lon1 = np.radians(slong)
    lat2 = np.radians(dlat)
    lon2 = np.radians(dlong)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    conv_fac = 0.621371
    miles = distance * conv_fac
    return miles <= dist
