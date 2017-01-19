import os

"""
Setting the utility tools
"""

def get_imlist(path):
    """
    Get the all jpg file list
    :param path:
    :return:
    """
    return [os.path.join(path, f) for f in os.listdir(path) if f.endwith(".jpg")]