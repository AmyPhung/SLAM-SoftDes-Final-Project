from PIL import Image, ImageFont, ImageDraw
import textwrap

def navigator(start,finish):
    lineWidth = 2
    map = Image.open("Maps/MapNon-Fill.png")
    solution = map
    slope = (start[1] - finish[1]) / (start[0] - finish[0])
    b = start[1] - slope * start[0]
    x_size = map.size[0]
    y_size = map.size[1]
    for x in range(x_size):
        for y in range(y_size):
            if(abs(y - (slope * x + b)) < lineWidth and ((x < finish[0] and x > start[0]) or (x < start[0] and x > finish[0]))
            and ((y < finish[1] and y > start[1]) or (y < start[1] and y > finish[1]) )):
                solution.putpixel((x, y),(255, 0, 0))
            if(abs(x - start[0]) < 3 and abs(y - start[1]) < 3):
                solution.putpixel((x,y),(0,255,0))
            if(abs(x - finish[0]) < 3 and abs(y - finish[1]) < 3):
                solution.putpixel((x,y),(0,0,255))
    solution.save("Maps/solution.png")
if __name__ == '__main__':
    navigator((300,300),(600,200))
