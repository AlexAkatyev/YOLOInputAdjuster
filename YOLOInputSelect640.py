# Select the area with the 640 size marks on the large image
from PIL import Image
import os

# global parameters
windowSize = 640
margin = 5
sourceDir = 'd:/3'
resultDir = 'd:/4'

# gui color
startRed = '\033[31m'
startYellow = '\033[33m'
startGreen = '\033[32m'
endColor = '\033[0m'


def separatorPrint():
    print(startYellow + '----------------------------------------------------------------' + endColor)


def dirPathInput(defPath, preamble):
    result = defPath
    correct = False
    while not correct:
        print(preamble + f"(by default {defPath}) : ", end=' ')
        input_str = input()
        if input_str != '':
            if os.path.isdir(input_str):
                result = input_str
                correct = True
            else:
                print(startRed + 'input data not correct or directory not found' + endColor)
        else:
            if os.path.isdir(result):
                correct = True
            else:
                print(startRed + 'directory ' + result + ' not found' + endColor)
    print('----- set directory ' + startGreen + result + endColor)
    return result


def sourceDirPathInput():
    global sourceDir
    separatorPrint()
    sourceDir = dirPathInput(defPath=sourceDir, preamble='input source directory ')


def resultDirPathInput():
    global resultDir
    separatorPrint()
    resultDir = dirPathInput(defPath=resultDir, preamble='input result directory ')


def readMarkedline(stroka, w, h):
    result = []
    strarray = stroka.split()
    if len(strarray) < 5:
        return result
    # tag index 0
    centerx = round(float(strarray[1]) * w)
    centery = round(float(strarray[2]) * h)
    # width
    dwidth = round(float(strarray[3]) * w / 2)
    # height
    dheight = round(float(strarray[4]) * h / 2)
    result.append(centerx - dwidth)  # xl
    result.append(centery - dheight)  # yt
    result.append(centerx + dwidth)  # xr
    result.append(centery + dheight)  # yb
    return result


# tuples list
# tuple: (xleft, ytop, xright, ybottom)
def getCoordinates(imgname, markedname):
    global sourceDir
    global windowSize
    result = []
    img = Image.open(sourceDir + '/' + imgname)
    imgh = img.height
    imgw = img.width
    img.close()
    sourceMark = []
    fileName = os.path.join(sourceDir, markedname)
    if os.path.isfile(fileName):
        with open(fileName, 'r') as filer:
            liststr = filer.readlines()
            for i in range(len(liststr)):
                sourceMark.append(readMarkedline(liststr[i], imgw, imgh))
    xl = imgw
    xr = 0
    yt = imgh
    yb = 0
    for mark in sourceMark:
        if xl > mark[0]:
            xl = mark[0]
        if xr < mark[2]:
            xr = mark[2]
        if yt > mark[1]:
            yt = mark[1]
        if yb < mark[3]:
            yb = mark[3]

    x = (xl + xr) / 2
    y = (yt + yb) / 2
    ws = windowSize / 2
    result.append((x - ws, imgh / 2 - ws, x + ws, imgh / 2 + ws))
    return result


def correctFileName(fname, index):
    name, ext = os.path.splitext(fname)
    new_filename = f"{name}_s{index}{ext}"
    return new_filename


def selectImage(imgname, coordinates, iter):
    global sourceDir
    global resultDir
    global windowSize
    img = Image.open(sourceDir + '/' + imgname)
    cropped = img.crop(coordinates)
    cropped.save(resultDir + '/' + correctFileName(imgname, iter))


def run():
    global sourceDir
    separatorPrint()
    markedFiles = [f for f in os.listdir(sourceDir) if
                   (os.path.isfile(os.path.join(sourceDir, f)) and f.lower().endswith('.txt'))]
    count = len(markedFiles)
    i = 0
    print('Progress:')
    for markedName in markedFiles:
        if markedName.find('classes.txt') != -1:
            continue
        print(f"\r{i / count * 100:.2f} %   ", end='')
        imgName = markedName.lower().replace('.txt', '.png', -1)
        coordinatesList = getCoordinates(imgname=imgName, markedname=markedName)
        j = 1
        for positions in coordinatesList:
            selectImage(imgname=imgName, coordinates=positions, iter=j)
            j = j + 1
        i = i + 1
    print('\r' + startGreen + 'End of work' + endColor)


# MAIN BEGIN --------------------------------------------------------------
sourceDirPathInput()
resultDirPathInput()
run()
separatorPrint()
print('press enter to exit')
input()  # delay of user
# MAIN END __--------------------------------------------------------------
