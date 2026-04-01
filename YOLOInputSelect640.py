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


# tuples list
# tuple: (xleft, ytop, xright, ybottom)
def getCoordinates(imgname, merkedname):
    return [(100, 100, 740, 740), (200, 200, 840, 840)]


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
        print(f"\r{i / count * 100:.2f} %   ", end='')
        imgName = markedName.lower().replace('.txt', '.png', -1)
        coordinatesList = getCoordinates(imgname=imgName, merkedname=markedName)
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
