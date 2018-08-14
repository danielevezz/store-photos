import os
import datetime
from sys import argv

# Take directory from cli
PATH = argv[1]

# Go into that folder
os.chdir(PATH)

# Take all filenames
imageList = os.listdir()

# Filter out all directories
imageList = [str(img) for img in imageList if not os.path.isdir(img)]

for img in imageList:
    imgPath = PATH + img

    if "_" in img:
        date = img.split("_")[1]
        date = date.split("-")[0]
    else:
        date = img.split("-")[1]

    print(date)
    
    shotDate = datetime.datetime.strptime(
                date, "%Y%m%d")

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