import os
import datetime
from PIL import Image, ExifTags
from sys import argv

# Take directory from cli
PATH = argv[1]

# Go into that folder
os.chdir(PATH)

# Take all filenames
imageList = os.listdir()

# Filter out all .png
imageList = [str(img) for img in imageList if ".png" not in str(img)]
print(f"There are {len(imageList)} elements in this folder")

for img in imageList:
    # Filter out all folders
    if os.path.isdir(img):
        continue

    # Create path for image
    imgPath = PATH + img

    tmp = Image.open(imgPath)
    # Get exif data from that image
    tags = tmp._getexif()

    # If there is data then create a dictionary with it
    if tags is not None:
        exif = {ExifTags.TAGS[k]: v for k,
                v in tags.items() if k in ExifTags.TAGS}

        # if there is date info then process it
        if "DateTime" in exif:
            photoDate = exif["DateTime"]
            shotDate = datetime.datetime.strptime(
                photoDate, "%Y:%m:%d %H:%M:%S")

            # the folder is named after the date
            folderName = f"{shotDate:%d-%m-%Y}"

            # if the folder already exists then do not create it
            if not os.path.isdir(folderName):
                print(f"Create folder {folderName}")
                os.mkdir(folderName)
            imgName = str(img)

            # move the file into the directory
            os.rename(imgPath, PATH + folderName + "/" + imgName)
            print(f"Moved {imgName} into {folderName}")
