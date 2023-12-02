import cv2 as cv
import numpy as np

from models.color import Color


def get_img_with_color(img, lower_color, upper_color):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_color, upper_color)
    return cv.bitwise_and(img, img, mask=mask)


def get_color_coverage(img, lower_color, upper_color):
    output = get_img_with_color(img, lower_color, upper_color)
    total_pixel_count = output.size
    color_pixel_count = np.count_nonzero(output)
    return 100 / total_pixel_count * color_pixel_count


def check_blue(img):
    return get_color_coverage(img, (100, 50, 50), (130, 255, 255)) > 70


def check_yellow(img):
    return get_color_coverage(img, (20, 100, 100), (40, 255, 255)) > 70


def check_red(img):
    red_mask1 = get_img_with_color(img, (0, 100, 100), (10, 255, 255))
    red_mask2 = get_img_with_color(img, (160, 100, 100), (180, 255, 255))
    output = cv.bitwise_or(red_mask1, red_mask2)
    total_pixel_count = output.size
    color_pixel_count = np.count_nonzero(output)
    color_coverage = 100 / total_pixel_count * color_pixel_count
    return color_coverage > 70


def get_color(img):
    if check_blue(img):
        return Color.BLUE
    if check_red(img):
        return Color.RED
    if check_yellow(img):
        return Color.YELLOW
    return Color.NONE


def get_positions(img):
    upper_left = img[260:330, 750:820]
    lower_left = img[410:460, 750:820]

    upper_right = img[260:330, 1100:1170]
    lower_right = img[410:460, 1100:1170]

    print("UPPER LEFT", get_color(upper_left))
    print("LOWER LEFT", get_color(lower_left))
    print("UPPER RIGHT", get_color(upper_right))
    print("LOWER RIGHT", get_color(lower_right))


cap = cv.VideoCapture('assets/pren_cube_01.mp4')

# pren_cube_01.mp4
#cap.set(1, 110)
#cap.set(1, 330)
#cap.set(1, 560)
#cap.set(1, 895)

# pren_cube_02.mp4
#cap.set(1, 325)
#cap.set(1, 660)
#cap.set(1, 885)


cap.set(1, 102)
ret, frame = cap.read()
get_positions(frame)
cv.imshow('output', frame)
cv.waitKey()

cap.set(1, 325)
_, frame = cap.read()
get_positions(frame)
cv.imshow('output', frame)
cv.waitKey()

cap.set(1, 548)
_, frame = cap.read()
get_positions(frame)
cv.imshow('output', frame)
cv.waitKey()

cap.set(1, 771)
_, frame = cap.read()
get_positions(frame)
cv.imshow('output', frame)
cv.waitKey()

#cv.line(frame, (0, 260), (2000, 260), (255, 255, 255), 1)
#cv.line(frame, (0, 330), (2000, 330), (255, 255, 255), 1)


#cv.line(frame, (0, 410), (2000, 410), (255, 0, 255), 1)
#cv.line(frame, (0, 460), (2000, 460), (255, 0, 255), 1)


#cv.line(frame, (750, 0), (750, 2000), (255, 255, 0), 1)
#cv.line(frame, (820, 0), (820, 2000), (255, 255, 0), 1)

#cv.line(frame, (1100, 0), (1100, 2000), (255, 255, 0), 1)
#cv.line(frame, (1170, 0), (1170, 2000), (255, 255, 0), 1)

cv.imshow('output', frame)
cv.waitKey()
