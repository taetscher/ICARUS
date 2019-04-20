# from https://github.com/markjay4k/YOLO-series/blob/master/part6%20-%20draw_box_py36.py
"""This Program lets you automate the writing of xml files needed for training yolo"""

import os
import matplotlib.pyplot as plt
import cv2
from matplotlib.widgets import RectangleSelector
from generate_xml import write_xml
from datetime import datetime


start = datetime.now()

# global constants
img = None
tl_list = []
br_list = []
object_list = []



# set batch number folder here!
# log:
# Batch 1 [x]
# Batch 2 []
# Batch 3 []
# Batch 4 []
# Batch 5 []
# Batch 6 []
# Batch 7 []
# Batch 8 []
# Batch 9 []
# Batch 10 []
# Batch 11 []
# Batch 12 []
# Batch 13 []
# Batch 14 []
# Batch 15 []
# Batch 16 []
# Batch 17 []
# Batch 18 []
# Batch 19 []
# Batch 20 []
# Batch 21 []
# Batch 22 []
# Batch 23 []
# Batch 24 []
# Batch 25 []
# Batch 26 []
# Batch 27 []



batch = 2

image_folder = 'fullTrainingDataset/batch{}'.format(str(batch))
savedir = 'annotations'
obj = 'all_Season_Road'


def line_select_callback(clk, rls):
    global tl_list
    global br_list
    global object_list
    tl_list.append((int(clk.xdata), int(clk.ydata)))
    br_list.append((int(rls.xdata), int(rls.ydata)))
    object_list.append(obj)


def onkeypress(event):
    global object_list
    global tl_list
    global br_list
    global img
    if event.key == 'q':
        print(object_list)
        write_xml(image_folder, img, object_list, tl_list, br_list, savedir)
        tl_list = []
        br_list = []
        object_list = []
        img = None


def toggle_selector(event):
    toggle_selector.RS.set_active(True)


if __name__ == '__main__':
    for n, image_file in enumerate(os.scandir(image_folder)):
        img = image_file
        fig, ax = plt.subplots(1, figsize=(10.5, 8))
        image = cv2.imread(image_file.path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        ax.imshow(image)

        #draw the actual box onscreen
        toggle_selector.RS = RectangleSelector(
            ax, line_select_callback,
            drawtype='box', useblit=True,
            button=[1], minspanx=5, minspany=5,
            spancoords='pixels', interactive=True,
        )

        bbox = plt.connect('key_press_event', toggle_selector)
        key = plt.connect('key_press_event', onkeypress)
        plt.tight_layout()
        plt.show()
        plt.close(fig)
stop = datetime.now()
print("program finished, time elapsed: ", stop-start)