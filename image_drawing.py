import os
import cv2
import sys
import pyautogui
import time
import json

'''
for pyautogui, please refer to this doc:
https://pyautogui.readthedocs.io/en/latest/quickstart.html

run test 
image_drawing.py image-file, func [0:drag_draw, 1:mouse_click]
python image_drawing.py "IMG_825.jpg" 0
'''
imagefile = "IMG_825.jpg"

def convert_image_to_array(imagefile):
    draw_line = []
    # read imagefile
    original = cv2.imread(imagefile)
    gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    _, blackAndWhiteImage = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow('black & white image', blackAndWhiteImage)
    # click to start conversion
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

    y_total = len(blackAndWhiteImage)
    for y in range(y_total):
        row = blackAndWhiteImage[y]
        # initial _x_start = -1
        _x_start,_x_end = -1,0
        for x in range(len(row)):
            if row[x] == 0:     # drawing point
                if _x_start == -1:
                    _x_start = x      # start drawing point
                    _x_end = x
                else:
                    _x_end = x
            else:
                if _x_start >= 0:
                    draw_line.append([_x_start, _x_end, y])
                    _x_start = -1
            if x == len(row)-1 and _x_start >=0:
                draw_line.append([_x_start, _x_end, y])
                _x_start = -1
    # save the draw_line to file.
    arrayfile = f'{imagefile}.txt'
    with open(arrayfile,'w') as f :
        json.dump(draw_line, f)
    print(f'processing the image and save it to {arrayfile}')
    return arrayfile

class draw():
    def __init__(self, x_start,y_start):
        pyautogui.PAUSE = 2.5
        pyautogui.FAILSAFE = True
        self.x=x_start
        self.y=y_start

    def abs_position(self, d):
        return self.x + d[0],self.x + d[1], self.y + d[2]

    def drag_draw(self, d):   # d[0] x_start, d[1] x_end, d[2] y
        xs, xe, y = self.abs_position(d)
        pyautogui.moveTo(xs, y)

        pyautogui.dragTo(xe, y)

    def mouse_tick(self, d):
        xs, xe, y = self.abs_position(d)
        for x in range(xs,xe):
            pyautogui.click(x, y)

if __name__ == '__main__':
    imagefile = 
    arrayfile = f"{imagefile}.txt"
    if not os.path.isfile(arrayfile):
        arrayfile = convert_image_to_array(imagefile)

    x_start = 1000
    y_start = 500
    image_array = sys.argv[1]
    func = sys.argv[2]
    with open(arrayfile, "r") as f:
        image_array = json.load(f)

    my_draw = draw(x_start,y_start)
    i = 0
    for d in image_array:
        if i % 10 == 0: 
            print(f'drawing dataset: {d}')
            time.sleep(0.005)
        if func == 0 :
            my_draw.drag_draw(d)
        elif func == 1 :
            my_draw.mouse_tick(d)
        
        i += 1

