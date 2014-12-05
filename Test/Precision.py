__author__ = 'endru'
import math
import camera
import ContourFinder as cf
import cv2
import cv2.cv as cv
import numpy as np
import time
from video import create_capture


threshold_val = 70
cnt_calculator = cf.ContourCalc(cf.Rect(640, 480), cf.Field(0, 0, 640, 480), cf.Rect(100,120))

cam = create_capture('synth:bg=/home/endru/Documents/Development/precision_images/640_480_pic00003.jpg', fallback='synth:bg=../cpp/lena.jpg:noise=0.05')

while True:
    ret, img = cam.read()
    cnt_info = cnt_calculator.find_contours(img, True)

    k = 0xFF & cv2.waitKey(5)
    if k != 255:
        print k
    if k == 27:
        print 'escape'
        break
    if k == 114:
        cnt_calculator.field_top_up()
        print 'field top up  ' + str(cnt_calculator.field.y)
    if k == 102:
        cnt_calculator.field_top_down()
        print 'field top down ' + str(cnt_calculator.field.y)
    if k == 117:
        cnt_calculator.field_bottom_up()
        print 'field bottom up ' + str(cnt_calculator.field.y)
    if k == 106:
        cnt_calculator.field_bottom_down()
        print 'field bottom down ' + str(cnt_calculator.field.y)
    if k == 81:
        cnt_calculator.threshold_decrease()
        print 'threshold down ' + str(cnt_calculator.threshold)
    if k == 83:
        cnt_calculator.threshold_increase()
        print 'threshold up ' + str(cnt_calculator.threshold)

    if cnt_info is None:
        continue

    print '%s\r' % ' '*20, # clean up row
    print 'distance: %.lf px' % cnt_info.center_distance.x + '\t |\t area: %.lf px' % cnt_info.area,

cv2.destroyAllWindows()