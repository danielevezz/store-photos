import os
import datetime
from PIL import Image, ExifTags

PATH = "/home/danielevezz/Pictures/"

os.chdir(PATH)
imageList = os.listdir()

for img in imageList:
    imgPath = PATH + str(img) 
    if ".jpg" not in imgPath or ".jpeg" not in imgPath:
        continue
    print(imgPath)

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
            os.rename(imgPath, PATH + folderName + "/" + str(img))
        if "Model" in exif:
            print(exif["Model"])
        if "Make" in exif:
            print(exif["Make"])
        if "GPSInfo" in exif:
            print(exif["GPSInfo"])