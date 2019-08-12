from exif import Image
import os


def map(folder):
    for root, dirs, files in os.walk(folder):
        for fname in files:
            print(os.path.join(root, fname))
            with open(os.path.join(root, fname), "rb") as f:
                img = Image(f)
                if not img.has_exif:
                    continue

                print("({img.gps_latitude}, {img.gps_longitude})")
        for dname in dirs:
            print(os.path.join(root, dname))
