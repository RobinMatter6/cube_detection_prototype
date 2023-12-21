import cv2
import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))


# initialize the WindowCapture class
video_path = '../../assets/pren_cube_01.mp4'
wincap = cv2.VideoCapture(video_path)

# initialize the Vision class
vision_limestone = Vision('../../assets/haystack_img/blue_block_mask.jpg')

# initialize the trackbar window
vision_limestone.init_control_gui()

# limestone HSV filter
hsv_filter = HsvFilter(58, 66, 0, 130, 255, 255, 0, 0, 0, 0)
#hsv_filter = HsvFilter(90, 0, 0, 115, 255, 255, 75, 0, 255, 0)

loop_time = time()
while(True):

    # get an updated image of the game
    ret, frame = wincap.read()

    # pre-process the image
    processed_image = vision_limestone.apply_hsv_filter(frame, hsv_filter)

    # do object detection
    rectangles = vision_limestone.find(processed_image, 0.5)

    # draw the detection results onto the original image
    output_image = vision_limestone.draw_rectangles(frame, rectangles)

    # display the processed image
    cv.imshow('Processed', processed_image)
    cv.imshow('Matches', output_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
