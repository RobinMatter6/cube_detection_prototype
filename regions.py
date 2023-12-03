from datetime import datetime

import cv2 as cv
import numpy as np
import requests

from models.color import Color
from models.direction import Direction


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


def get_positions(img, direction, config):
    upper_left = img[260:330, 750:820]
    lower_left = img[410:460, 750:820]

    upper_right = img[260:330, 1100:1170]
    lower_right = img[410:460, 1100:1170]

    lower_left_color = get_color(lower_left)
    if direction == direction.FRONT:
        config[3] = lower_left_color
    if direction == direction.RIGHT:
        config[0] = lower_left_color

    upper_left_color = get_color(upper_left)
    if direction == direction.FRONT:
        config[7] = upper_left_color
    if direction == direction.RIGHT:
        config[4] = upper_left_color

    lower_right_color = get_color(lower_right)
    if direction == direction.FRONT:
        config[1] = lower_right_color
    if direction == direction.RIGHT:
        config[2] = lower_right_color

    upper_right_color = get_color(upper_right)
    if direction == direction.FRONT:
        config[5] = upper_right_color
    if direction == direction.RIGHT:
        config[6] = upper_right_color

    return config


cap = cv.VideoCapture('assets/pren_cube_01.mp4')

config = [Color.UNDEFINED] * 8

cap.set(1, 102)
_, frame = cap.read()
config = get_positions(frame, Direction.FRONT, config)

cap.set(1, 325)
_, frame = cap.read()
config = get_positions(frame, Direction.RIGHT, config)

url = "http://18.192.48.168:5000/cubes/team05"
headers = {
    "Content-Type": "application/json",
    "Auth": "test1234"
}
body = {
    'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'config': {
        '1': str(config[0]),
        '2': str(config[1]),
        '3': str(config[2]),
        '4': str(config[3]),
        '5': str(config[4]),
        '6': str(config[5]),
        '7': str(config[6]),
        '8': str(config[7]),
    }
}

response = requests.post(url, json=body, headers=headers)
print(response.status_code)
