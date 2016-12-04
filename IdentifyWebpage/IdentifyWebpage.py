"""
IdentifyWebpage.py
~~~~~~~~~~~~~~~~~
This program is a demo, it is used to make sure Android's Browser app has loaded a webpage successfully.
The webpage is an empty page with green background, after the Browser app load the page, use adb command
to take a snapshot and copy it to pc local. Then, this program will load this picture and see if it is
full of green. If so, the webpage is loaded successfully.
"""
from PIL import Image
import os


class IdentifyWebpage(object):
    def __init__(self):
        self.points = [(200, 300), (455, 678), (333, 1200),
                       (300, 500), (888, 678), (900, 800),
                       (400, 600), (245, 365), (799, 777)]

    def get_snapshot(self):
        os.system('adb shell /system/bin/screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png ~/Project/IndenfyWebpage/screenshot.png')

    def indenfy(self):
        result = []
        img = Image.open('snapshot.png')
        for point in self.points:
            color = img.getpixel(point)
            result.append(color)
        if len(set(result)) == 1:
            print('As the 9 points in the snapshot have the same RGB values,'
                  'I can assert that the web page is loaded successfully.\n'
                  '截图中9个点的RGB值完全一样，可以认为是一张纯色的截图。')

if __name__ == '__main__':
    identifier = IdentifyWebpage()
    identifier.get_snapshot()
    identifier.indenfy()