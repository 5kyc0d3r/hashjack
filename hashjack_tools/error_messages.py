from colors import *


def success(message):
    return '[' + green + '+' + white + '] ' + str(message)


def info(message):
    return '[' + blue + '+' + white + '] ' + str(message)


def warning(message):
    return '[' + yellow + '!' + white + '] ' + str(message)


def error(message):
    return '[' + red + '-' + white + '] ' + str(message)
