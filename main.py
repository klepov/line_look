import cv2
import numpy as np
import scipy
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

# img = cv2.imread('test.png',0)
# edges = cv2.Canny(img,150,70,)
#
# plt.subplot(121),plt.imshow(img,cmap = 'gray')
# plt.title('Original Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(edges,cmap = 'gray')
# plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
# plt.show()

from numpy.core.tests.test_mem_overlap import xrange
from scipy.misc import toimage


def thresh_callback(thresh, img, color):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, thresh, thresh * 2)
    _, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        cv2.drawContours(img, [cnt], 0, color, 2)
        # cv2.imshow('output',drawing)
        cv2.imwrite('final.jpg', img)

    return 'final.jpg'


def draw_counter(image, thresh_gui, color):
    # thresh = int(100*thresh_gui)
    thresh_callback(thresh_gui, cv2.imread(image),color)
