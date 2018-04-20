from PIL import Image
import cv2

class Map:
    def __init__(self,filename):
        self.map_img = filename

    def convert_pgm_to_png(self):
        im = Image.open(self.map_img)
        color_im = cv2.cvtColor(im, cv2.CV_GRAY2RGB)
        print(color_im)
        color_im.save('./Maps/map.png')



if __name__ == '__main__':
    lib = Map('./Maps/library_lower.pgm')
    lib.convert_pgm_to_png()

