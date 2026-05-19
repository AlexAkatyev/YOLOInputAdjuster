# разделить размеченные файлы для тренировки и валидации

from ultralytics.data.split import autosplit
import os


sourceDir = '.'

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


sourceDirPathInput()
autosplit(
    path=sourceDir,
    weights=(0.8, 0.2, 0.0),  # (train, validation, test) fractional splits
    # !!!! Разделять только изображения с файлом аннотаций, если установлено значение True.
    annotated_only=False,  # split only images with annotation file when True
)
