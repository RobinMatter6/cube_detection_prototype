import numpy as np
import cv2 as cv

from models.color import Color
from models.contour import Contour
from models.position import Position


def get_img_with_color(img, lower_color, upper_color):
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    mask = cv.inRange(hsv, lower_color, upper_color)
    return cv.bitwise_and(img, img, mask=mask)


def grayscale_img(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def blur_img(img, size):
    return cv.blur(img, (size, size))


def prepare_img(img, lower_color, upper_color, blur):
    result = get_img_with_color(img, lower_color, upper_color)
    result = grayscale_img(result)
    result = blur_img(result, blur)
    return result


def get_contours(img, threshold, color):
    _, thresh = cv.threshold(img, threshold, threshold * 2, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    final_contours = []
    for i in range(len(contours)):
        approx = cv.approxPolyDP(
            contours[i], 0.01 * cv.arcLength(contours[i], True), True)

        area = cv.contourArea(approx)
        if area < 10_000:
            continue

        m = cv.moments(approx)
        center_x = int(m["m10"] / m["m00"])
        center_y = int(m["m01"] / m["m00"])

        final_contours.append(Contour(area, (center_x, center_y), color))
    return final_contours


def draw_contours(contours, color):
    for i in range(len(contours)):
        approx = cv.approxPolyDP(
            contours[i], 0.01 * cv.arcLength(contours[i], True), True)

        cv.drawContours(frame, [approx], 0, color, 1)


def get_center_of_contour(contour):
    m = cv.moments(contour)
    c_x = int(m["m10"] / m["m00"])
    c_y = int(m["m01"] / m["m00"])

    return c_x, c_y


def calc_positions(contours):
    sorted_contours = sorted(contours, key=Contour.get_center_y, reverse=True)
    for contour in sorted_contours:
        #print(str(contour.get_center_x()) + " " + str(contour.get_center_y()), " " + str(contour.color))
        cv.circle(frame, contour.center, 2, (255, 255, 255), 2)

        message = ""
        if contour.area > 50_000:
            position = Position.STACKED
        else:
            if contour.get_center_y() > 500:
                message += "FRONT BOTTOM"
            else:
                if contour.get_center_y() > 450:
                    message += "FRONT BOTTOM"
                else:
                    if contour.get_center_y() > 310:
                        message += "FRONT TOP"
                    else:
                        if contour.get_center_y() > 280:
                            message += "BACK BOTTOM"
                        else:
                            if contour.get_center_y() > 210:
                                message += "BACK TOP"
                            else:
                                if contour.get_center_y() > 130:
                                    message += "BACK TOP"

            if contour.get_center_x() > 1000:
                message += " RIGHT"
            else:
                message += " LEFT"

        print(message, contour.color)


def process(frame):
    blue_img = prepare_img(frame, (100, 50, 50), (130, 255, 255), 3)

    red_mask1 = get_img_with_color(frame, (0, 100, 100), (10, 255, 255))
    red_mask2 = get_img_with_color(frame, (160, 100, 100), (180, 255, 255))
    red_mask = cv.bitwise_or(red_mask1, red_mask2)
    red_img = blur_img(grayscale_img(red_mask), 3)

    yellow_img = prepare_img(frame, (20, 100, 100), (40, 255, 255), 3)

    blue_contours = get_contours(blue_img, 10, Color.BLUE)
    red_contours = get_contours(red_img, 10, Color.RED)
    yellow_contours = get_contours(yellow_img, 10, Color.YELLOW)

    contours = blue_contours + red_contours + yellow_contours
    calc_positions(contours)

cap = cv.VideoCapture('assets/pren_cube_01.mp4')

# pren_cube_01.mp4
cap.set(1, 220)
#cap.set(1, 445)
#cap.set(1, 670)
#cap.set(1, 895)

# pren_cube_02.mp4
#cap.set(1, 210)
#cap.set(1, 435)
#cap.set(1, 660)
#cap.set(1, 885)


ret, frame = cap.read()
process(frame)
cv.imshow('output', frame)
cv.waitKey()

cap.set(1, 445)
ret, frame = cap.read()
process(frame)
cv.imshow('output', frame)
cv.waitKey()

cap.set(1, 670)
ret, frame = cap.read()
process(frame)
cv.imshow('output', frame)
cv.waitKey()

cap.set(1, 895)
ret, frame = cap.read()
process(frame)
cv.imshow('output', frame)
cv.waitKey()



