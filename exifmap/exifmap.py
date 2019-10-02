from exif import Image
import os
import re
from urllib.parse import urlencode

# Get a query URL for Google Maps Static API
def map_url(data, api_key, width=500, height=500, map_type="roadmap"):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    params = {
        "size": f"{width}x{height}",
        "key": api_key,
        "maptype": map_type,
        "markers": [],
    }
    for f, d in data.items():
        lat = d.get("latitude")
        lon = d.get("longitude")
        if lat is None or lon is None:
            continue

        params["markers"].append("{0:.6f},{1:.6f}".format(lat, lon))

    params["markers"] = "|".join(params["markers"])
    param_str = urlencode(params)
    full_url = base_url + param_str
    print(full_url)
    return full_url


# Construct base marker query param
# TODO: implement
def _markerq_base(size="normal", color=None, label=None):
    pass


# Return a dictionary with geo-locations of files rooted at given directory
def exif(folder, recurse=True):
    data = dict()
    for root, dirs, files in os.walk(folder):
        for fname in files:
            fpath = os.path.join(root, fname)
            with open(fpath, "rb") as f:
                img = Image(f)
                if not img.has_exif:
                    continue

                data[fpath] = _get_geo(img)
    return data


# Given an image return the dictionary containing relevant exif data
def _get_geo(img):
    d = {
        "latitude": _to_decimal(_get_exif_attr(img, "gps_latitude")),
        "longitude": _to_decimal(_get_exif_attr(img, "gps_longitude")),
        "time": _get_exif_time(img),
    }
    return d


# Convert degrees, minutes, seconds to decimal
def _to_decimal(geo):
    if geo is None:
        return None

    s = re.sub("[^0-9,.]", "", str(geo))
    bits = [float(x) for x in s.split(",")]
    d = sum([b / s for b, s in zip(bits, [1, 60.0, 3600.0])])
    return d


# Get an attribute from exif if available, None otherwise
def _get_exif_attr(img, attr):
    if attr in dir(img):
        return getattr(img, attr)
    else:
        return None


# Scan through different exif metadata fields for the
# earliest creation time
def _get_exif_time(img):
    pass
