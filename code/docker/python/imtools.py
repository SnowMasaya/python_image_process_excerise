import os
import numpy

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

def imresize(im, sz):
    """
    Resize the Image
    :param im(array): image data
    :parama sz(int): set the resize value 
    :return(array): return the image array 
    """
    pil_im = Image.fromarray(uint8(im))
    return array(pil_im.resize(sz))

def histeq(im, nbr_bins=256):
    """
    Flattern the gray scale image
    get the Image histogram
    :param im(array): image data
    :param nbr_bins: set the bins
    :return : histogram and gray scale image
    """
    imhist, bins = numpy.histogram(im.flatten(), nbr_bins, normed=True)
    cdf = imhist.cumsum()
    cdf = 255 * cdf / cdf[-1]
    
    im2 = interp(im.flatten(), bins[:-1], cdf)
    
    return im2.reshape(im.shape), cdf

def compute_average(imlist):
    """
    get the average the image
    :param(list): get the image list
    :return(array): average image data
    """
    averageim = array(Image.open(imlist[0]), "f")
    for imname in imlist[1:]:
        try:
            averageim += array(Image.open(imname))
        except:
            print(imname + "..skiped")
    averageim /= len(imlist)
    
    return array(averageim, "uint8")
