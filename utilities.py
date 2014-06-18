import os

def flip_boolean(value):
    if value:
        return False
    else:
        return True

def get_imlist(path, file_type):
    """ Returns a list of filenames for
    all jpg images in a directory. """
    return [os.path.join(path,f) for f in os.listdir(path) if f.endswith('.' + file_type)]