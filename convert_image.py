import cv2

"""
Author: Sherrie Shen
This code converts a grayscale image to BGR and applies a Gaussian blur.
"""

class Map:
    def __init__(self, filename):
        self.map_img = filename

    def convert_pgm_to_png(self, name):
        im = cv2.imread(self.map_img, 0)
        color_im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR)
        blur_im = cv2.GaussianBlur(color_im, (5, 5), 0)
        cv2.imwrite('./Maps/%s' % name, blur_im)


if __name__ == '__main__':
    lib = Map('./Maps/library_lower_day2.pgm')
    lib.convert_pgm_to_png('library_lower_day2.png')
