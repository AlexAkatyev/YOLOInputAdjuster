# Выделяет из картинок в заданном каталоге квадрат указанного размера с заданной позиции
# Картинки складывет в отдельном каталоге

from PIL import Image
import os
import shutil


# global parameters
windowSize = 640
leftX = 0
topY = 0
sourceDir = '.'
resultDir = 'picked'

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


def setIntParameter(param, info):
    separatorPrint()
    result = param
    correct = False
    while not correct:
        print(f"input {info} (by default {result}) : ", end=' ')
        input_str = input()
        if input_str != '':
            if input_str.isdigit():
                result = int(input_str)
                correct = True
            else:
                print(startRed + 'input data not correct' + endColor)
        else:
            correct = True
    print(f"----- set {info} " + startGreen + f"{result}" + endColor)
    return result


def pickImage(imgName):
    global sourceDir
    global resultDir
    global windowSize
    img = Image.open(sourceDir + '/' + imgName)
    box = (leftX, topY, leftX + windowSize, topY + windowSize)
    cropped_img = img.crop(box)
    cropped_img.save(resultDir + '/' + imgName)


def run():
    global sourceDir
    global windowSize
    separatorPrint()
    images = [f for f in os.listdir(sourceDir) if (os.path.isfile(os.path.join(sourceDir, f)) and f.lower().endswith('.png'))]
    count = len(images)
    i = 0
    print('Progress:')
    for imgName in images:
        print(f"\r{i / count * 100:.2f} %   ", end='')
        pickImage(imgName)
        i = i + 1
    print('\r' + startGreen + 'End of work' + endColor)


# MAIN BEGIN --------------------------------------------------------------
sourceDirPathInput()
resultDirPathInput()
windowSize = setIntParameter(windowSize, 'windowSize')
leftX = setIntParameter(leftX, 'left x')
topY = setIntParameter(topY, 'top y')
run()
separatorPrint()
print('press enter to exit')
input()  # delay of user
# MAIN END __--------------------------------------------------------------
