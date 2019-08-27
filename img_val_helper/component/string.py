import os
import string


def split_path(s):
    return [x for x in s.split('/') if x]


def join_path(l):
    return '/' + '/'.join(l)


def get_exts(file_name):
    extensions = []
    while True:
        file_name, ext = os.path.splitext(file_name)
        if ext == "":
            break
        extensions.append(ext)
    return reversed(extensions)


def get_format_args(s):
    return [arg[1] for arg in string.Formatter().parse(s) if arg[1] is not None]


def progress(percent, num_of_symbols=50):
    done = int(num_of_symbols * percent)
    return "[{}{}] {:.2f}%".format('#' * done, ' ' * (num_of_symbols - done), percent * 100)
