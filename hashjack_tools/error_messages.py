from colors import *
from datetime import datetime


def success(message):
    return '[' + green + '+' + white + '] ' + str(message)


def info(message):
    return '[' + blue + '+' + white + '] ' + str(message)


def log(message):
    return '[' + green + '*' + white + '] ' + green + str(message) + white


def warning(message):
    return '[' + yellow + '!' + white + '] ' + str(message)


def error(message):
    return '[' + red + '-' + white + '] ' + str(message)


def hash_found(start_time, hash_value, current_word):
    stop_time = datetime.now()
    total_time = stop_time - start_time
    print(success(green + bold + 'Password hash match found at {}.'.format(datetime.now()) + white))
    print(success(green + bold + 'Total running time (H:M:S:MS): {}.'.format(total_time) + white))
    print(success(green + bold + 'Hash: {} => Value: {}\n'.format(hash_value, current_word) + white))


def hash_not_found(start_time):
    stop_time = datetime.now()
    total_time = stop_time - start_time
    print(success(green + bold + 'Finished at: {}.'.format(stop_time) + white))
    print(success(green + bold + 'Total running time (H:M:S:MS): {}.'.format(total_time) + white))
    print(error(red + bold + 'Password hash could not be found.\n' + white))
