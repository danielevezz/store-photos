import os
import datetime
from PIL import Image, ExifTags
from sys import argv
import pprint
from geopy.geocoders import Photon
from geopy.point import Point

def convert_to_degrees(value):
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)

PATH = argv[1]

os.chdir(PATH)
imageList = os.listdir()

for img in imageList:
    if os.path.isdir(img):
        continue
    imgPath = PATH + str(img) 
    if ".png" in imgPath:
        continue

    tmp = Image.open(imgPath)
    tags = tmp._getexif()
    if tags is not None:
        exif = { ExifTags.TAGS[k]: v for k, v in tags.items() if k in ExifTags.TAGS }
        #print(exif)
        if "DateTime" in exif:
            photoDate = exif["DateTime"]
            shotDate = datetime.datetime.strptime(photoDate, "%Y:%m:%d %H:%M:%S")
            folderName = f"{shotDate:%d-%m-%Y}"
            if os.path.isdir(folderName):
                print("Folder already present")
            else:
                os.mkdir(folderName)
            #os.rename(imgPath, PATH + folderName + "/" + str(img))
        if "Model" in exif:
            print(exif["Model"])
        if "Make" in exif:
            print(exif["Make"])
        if "GPSInfo" in exif:
            pp = pprint.PrettyPrinter()
            gpsinfo = {}

            for key in exif['GPSInfo'].keys():
                decode = ExifTags.GPSTAGS.get(key,key)
                gpsinfo[decode] = exif['GPSInfo'][key]

            lat = str(convert_to_degrees(gpsinfo["GPSLatitude"]))
            lon = str(convert_to_degrees(gpsinfo["GPSLongitude"]))
            geolocator = Photon()
            location = geolocator.reverse(Point(lat,lon))
            altitude = location.altitude
            location = location.address.split(",")
            paese = location[5].strip()
            print(paese, altitude, sep=" ")



