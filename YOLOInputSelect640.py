# Select the area with the 640 size marks on the large image
from PIL import Image
import os
import shutil

# global parameters
windowSize = 640
margin = 0
sourceDir = 'd:/3'
resultDir = 'd:/4'

# gui color
startRed = '\033[31m'
startYellow = '\033[33m'
startGreen = '\033[32m'
endColor = '\033[0m'


def separatorPrint():
    print(startYellow + '----------------------------------------------------------------' + endColor)


def yMarginInput():
    global margin
    separatorPrint()
    correct = False
    while not correct:
        print(f"input window size (by default {margin}) : ", end=' ')
        input_str = input()
        if input_str != '':
            if input_str.isdigit():
                margin = int(input_str)
                correct = True
            else:
                print(startRed + 'input data not correct' + endColor)
        else:
            correct = True
    print('----- set window size ' + startGreen + f"{margin}" + endColor)


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


# out: list(tag, xl, yt, xr, yb)
def readMarkedline(stroka, w, h):
    result = []
    strarray = stroka.split()
    if len(strarray) < 5:
        return result
    # tag index 0
    result.append(int(strarray[0]))
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


# out: list list( tag, xl, yt, xr, yb)
def readmarkedFile(markedname, w, h):
    global sourceDir
    sourceMark = []
    fileName = os.path.join(sourceDir, markedname)
    if os.path.isfile(fileName):
        with open(fileName, 'r') as filer:
            liststr = filer.readlines()
            for i in range(len(liststr)):
                sourceMark.append(readMarkedline(liststr[i], w, h))
    return sourceMark


# (tuples list, imgw, imgh)
# tuple: (xleft, ytop, xright, ybottom)
def getCoordinates(imgname, markedname):
    global sourceDir
    global windowSize
    global margin
    result = []
    img = Image.open(sourceDir + '/' + imgname)
    imgh = img.height
    imgw = img.width
    img.close()
    sourceMark = readmarkedFile(markedname, imgw, imgh)
    xl = imgw
    xr = 0
    yt = imgh
    yb = 0
    for mark in sourceMark:
        if xl > mark[1]:
            xl = mark[1]
        if xr < mark[3]:
            xr = mark[3]
        if yt > mark[2]:
            yt = mark[2]
        if yb < mark[4]:
            yb = mark[4]
    hs = windowSize / 2
    listcx = []
    if xr - xl > windowSize:
        center = xl + hs
        listcx.append(center)
        while center + hs < xr:
            center += 1.5 * hs
            if center + hs > xr:
                center = xr - hs
            listcx.append(center)
    else:
        c0 = (xl + xr) / 2
        listcx.append(c0)
    for cx in listcx:
        result.append((cx - hs, imgh / 2 - hs, cx + hs, imgh / 2 + hs))
        if margin != 0:
            result.append((cx - hs, imgh / 2 - hs + margin, cx + hs, imgh / 2 + hs + margin))
    return result, imgw, imgh


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


def createLine(stroka, coord):
    global windowSize
    # check
    xl = stroka[1]
    yt = stroka[2]
    xr = stroka[3]
    yb = stroka[4]
    if xl >= coord[2]:
        return ''
    if yt >= coord[3]:
        return ''
    if xr <= coord[0]:
        return ''
    if yb <= coord[1]:
        return ''
    if xl < coord[0]:
        xl = coord[0]
    if yt < coord[1]:
        yt = coord[1]
    if xr > coord[2]:
        xr = coord[2]
    if yb > coord[3]:
        yb = coord[3]
    width = (xr - xl) / windowSize
    height = (yb - yt) / windowSize
    cx = (xl - coord[0]) / windowSize + width / 2
    cy = (yt - coord[1]) / windowSize + height / 2
    # tag
    result = str(stroka[0]) + ' '
    # cx
    result += "{:.6f}".format(cx) + ' '
    # cy
    result += "{:.6f}".format(cy) + ' '
    # width
    result += "{:.6f}".format(width) + ' '
    # height
    result += "{:.6f}".format(height)
    return result + '\n'


def createMarkToInput(markedname, coordinates, imgw, imgh, iter):
    global resultDir
    sourceMark = readmarkedFile(markedname, imgw, imgh)
    mark = ''
    for stroka in sourceMark:
        mark += createLine(stroka, coordinates)
    with open(correctFileName(resultDir + '/' + markedname, iter), "w", encoding="utf-8") as filew:
        filew.write(mark)


def run():
    global sourceDir
    global resultDir
    separatorPrint()
    markedFiles = [f for f in os.listdir(sourceDir) if
                   (os.path.isfile(os.path.join(sourceDir, f)) and f.lower().endswith('.txt'))]
    count = len(markedFiles)
    i = 0
    print('Progress:')
    for markedName in markedFiles:
        if markedName.find('classes.txt') != -1:
            shutil.copy(sourceDir + '/' + markedName, resultDir + '/' + markedName)
            continue
        print(f"\r{i / count * 100:.2f} %   ", end='')
        imgName = markedName.lower().replace('.txt', '.png', -1)
        (coordinatesList, iw, ih) = getCoordinates(imgname=imgName, markedname=markedName)
        j = 1
        for positions in coordinatesList:
            selectImage(imgname=imgName, coordinates=positions, iter=j)
            createMarkToInput(markedname=markedName, coordinates=positions, imgw=iw, imgh=ih, iter=j)
            j = j + 1
        i = i + 1
    print('\r' + startGreen + 'End of work' + endColor)


# MAIN BEGIN --------------------------------------------------------------
sourceDirPathInput()
resultDirPathInput()
yMarginInput()
run()
separatorPrint()
print('press enter to exit')
input()  # delay of user
# MAIN END __--------------------------------------------------------------
