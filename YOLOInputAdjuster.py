from PIL import Image
import os

# global parameters
inputWindowSize = 640
currentW = 640
currentH = 640
sourceDir = 'source'
resultDir = 'result'

# gui color
startRed = '\033[31m'
startYellow = '\033[33m'
startGreen = '\033[32m'
endColor = '\033[0m'


def separatorPrint():
    print(startYellow + '----------------------------------------------------------------' + endColor)


def windowSizeInput():
    global inputWindowSize
    separatorPrint()
    correct = False
    while not correct:
        print(f"input window size (by default {inputWindowSize}) : ", end=' ')
        input_str = input()
        if input_str != '':
            if input_str.isdigit():
                inputWindowSize = int(input_str)
                correct = True
            else:
                print(startRed + 'input data not correct' + endColor)
        else:
            correct = True
    print('----- set window size ' + startGreen + f"{inputWindowSize}" + endColor)


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


def correctImage(imgName):
    global sourceDir
    global resultDir
    global currentW
    global currentH
    img = Image.open(sourceDir + '/' + imgName)
    currentW = img.width
    currentH = img.height
    nimg = Image.new(mode='RGB', size=(inputWindowSize, inputWindowSize), color=(0, 0, 0))
    nimg.paste(img, box=(0, 0))
    nimg.save(resultDir + '/' + imgName)


def correctLine(stroka):
    global currentW
    global currentH
    strarray = stroka.split()
    if len(strarray) < 5:
        return stroka + '\n'
    # tag
    result = strarray[0] + ' '
    # x
    number = float(strarray[1]) * currentW / inputWindowSize
    result += str(number) + ' '
    # y
    number = float(strarray[2]) * currentH / inputWindowSize
    result += str(number) + ' '
    # width
    number = float(strarray[3]) * currentW / inputWindowSize
    result += str(number) + ' '
    # height
    number = float(strarray[4]) * currentH / inputWindowSize
    result += str(number)
    return result + '\n'


def correctMarkedText(imgName):
    global sourceDir
    global resultDir
    imgdown = imgName.lower()
    markedName = imgdown.replace('.png', '.txt', -1)
    fileName = os.path.join(sourceDir, markedName)
    if os.path.isfile(fileName):
        with open(fileName, 'r') as filer:
            liststr = filer.readlines()
            for i in range(len(liststr)):
                liststr[i] = correctLine(liststr[i])
            with open(os.path.join(resultDir, markedName), "w") as filew:
                filew.writelines(liststr)

def run():
    global sourceDir
    global inputWindowSize
    separatorPrint()
    markedImages = [f for f in os.listdir(sourceDir) if (os.path.isfile(os.path.join(sourceDir, f)) and f.lower().endswith('.png'))]
    count = len(markedImages)
    i = 0
    print('Progress:')
    for imgName in markedImages:
        print(f"\r{i / count * 100:.2f} %   ", end='')
        correctImage(imgName)
        correctMarkedText(imgName)
        i = i + 1
    print('\r' + startGreen + 'End of work' + endColor)



# MAIN BEGIN --------------------------------------------------------------
windowSizeInput()
sourceDirPathInput()
resultDirPathInput()
run()
separatorPrint()
print('press enter to exit')
input()  # delay of user
# MAIN END __--------------------------------------------------------------
