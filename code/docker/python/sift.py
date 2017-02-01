# -*- coding:utf-8 -*-
# !/usr/bin/python3

from PIL import Image
from numpy import *
from pylab import *
import os


def process_image(imagename, resultname, params="--edge--thresh 10 --peak-thresh 5"):
    """
    Process an image and save the result in a file
    :param imagename(str): set the input image name
    :param resultname: set the output feature name
    :param params:
    :return:
    """
    if imagename[-3:] != "pgm":
        im = Image.open(imagename).convert("L")
        im.save("tmp.pgm")
        imagename = "tmp.pgm"

    cmd = str("sift " + imagename + "--output=" + resultname +
              " " + params)
    os.system(cmd)
    print("processed ", imagename, " to " resultname)

def read_features_from_file(filename):
    """
    Read feature file
    :param filename(str): set the feature file name
    :return:
    """
    f = loadtxt(filename)
    return f[:,:4], f[:,4:]

def write_features_to_file(filename, locs, desc):
    """
    Write Feature file
    :param filename(str):
    :param locs(str):
    :param desc:
    :return:
    """
    savetxt(filename, hstack((locs, desc)))

def plot_features(im, locs, circle=False):
    """
    Show image with features,
    :param im: input image as array
    :param locs: (row, col, scale, orientation of each feature)
    :param circle:
    :return:
    """
    def draw_circle(c, r):
        t = arrange(0, 1.01, .01) * 2 * pi
        x = r * cos(t) + c[0]
        y = r * sin(t) + c[1]
        plot(x, y, "b", linewidth=2)

    imshow(im)
    if circle:
        for p in locs:
            draw_circle(p[:2], p[2])
    else:
        plot(locs[:, 0], locs[:, 1], "ob")
    axis("off")

def match(desc1, desc2):
    """
    For each descriptor in the first image, se
    :param desc1:
    :param desc2:
    :return:
    """
