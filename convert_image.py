from PIL import Image

class Map:
    def __init__(self,filename):
        self.map_img = filename

    def convert_pgm_to_png(self):
        im = Image.open(self.map_img)
        im.save('/Maps/map.png')



if __name__ == '__main__':
    lib = Map('/Maps/library_lower.pgm')
    lib.convert_pgm_to_png()

