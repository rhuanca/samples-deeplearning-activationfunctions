#!/usr/bin/python3
import wget
import os
import gzip
import shutil

import struct
import numpy as np


mnist_url = "http://yann.lecun.com/exdb/mnist"
train_images_filename = "train-images-idx3-ubyte"
train_labels_filename = "train-labels-idx1-ubyte"
test_images_filename = "t10k-images-idx3-ubyte"
test_labels_filename = "t10k-labels-idx1-ubyte"

def mnist_decompress(file_in, file_out):
    with gzip.open(file_in, 'rb') as f_in:
            with open(file_out, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

def mnist_download(data_dir, download_dir="download"):
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    wget.download( "%s/%s.gz" % (mnist_url, train_images_filename), out=download_dir)
    wget.download( "%s/%s.gz" % (mnist_url, train_labels_filename), out=download_dir)
    wget.download( "%s/%s.gz" % (mnist_url, test_images_filename), out=download_dir)
    wget.download( "%s/%s.gz" % (mnist_url, test_labels_filename), out=download_dir)

    mnist_decompress("%s/%s.gz" % (download_dir, train_images_filename), "%s/%s" % (data_dir, train_images_filename))
    mnist_decompress("%s/%s.gz" % (download_dir, train_labels_filename), "%s/%s" % (data_dir, train_labels_filename))
    mnist_decompress("%s/%s.gz" % (download_dir, test_images_filename), "%s/%s" % (data_dir, test_images_filename))
    mnist_decompress("%s/%s.gz" % (download_dir, test_labels_filename), "%s/%s" % (data_dir, test_labels_filename))

    return {
        "train_images": train_images_filename,
        "train_labels": train_labels_filename,
        "test_images" : test_images_filename,
        "test_labels" : test_labels_filename
    }
    

#
# IMPORTANT:
# The next two functions are copy of https://gist.github.com/akesling/5358964
#
# These where copied here to allow parse and read mnist data set
#

"""
Loosely inspired by http://abel.ee.ucla.edu/cvxopt/_downloads/mnist.py
which is GPL licensed.
"""

def read(dataset = "training", path = "."):
    """
    Python function for importing the MNIST data set.  It returns an iterator
    of 2-tuples with the first element being the label and the second element
    being a numpy.uint8 2D array of pixel data for the given image.
    """

    if dataset is "training":
        fname_img = os.path.join(path, 'train-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 'train-labels-idx1-ubyte')
    elif dataset is "testing":
        fname_img = os.path.join(path, 't10k-images-idx3-ubyte')
        fname_lbl = os.path.join(path, 't10k-labels-idx1-ubyte')
    else:
        raise ValueError("dataset must be 'testing' or 'training'")

    # Load everything in some numpy arrays
    with open(fname_lbl, 'rb') as flbl:
        magic, num = struct.unpack(">II", flbl.read(8))
        lbl = np.fromfile(flbl, dtype=np.int8)

    with open(fname_img, 'rb') as fimg:
        magic, num, rows, cols = struct.unpack(">IIII", fimg.read(16))
        img = np.fromfile(fimg, dtype=np.uint8).reshape(len(lbl), rows, cols)

    get_img = lambda idx: (lbl[idx], img[idx])

    # Create an iterator which returns each image in turn
    for i in range(len(lbl)):
        yield get_img(i)

def show(image):
    """
    Render a given numpy.uint8 2D array of pixel data.
    """
    from matplotlib import pyplot
    import matplotlib as mpl
    fig = pyplot.figure()
    ax = fig.add_subplot(1,1,1)
    imgplot = ax.imshow(image, cmap=mpl.cm.Greys)
    imgplot.set_interpolation('nearest')
    ax.xaxis.set_ticks_position('top')
    ax.yaxis.set_ticks_position('left')
    pyplot.show()
