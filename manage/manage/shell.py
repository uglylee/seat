#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
重设图像大小。
缩小图像，比例为（0.3, 0.5）
放大图像，比例为（1.6, 1.2）
"""



import cv2
import os

if __name__ == '__main__':
    for img in ['waitSeat']:
    # for img in ['floor']:
        image = cv2.imread('../static/images/%s.png' %(img),cv2.IMREAD_UNCHANGED)
        res = cv2.resize(image, (80,80), interpolation=cv2.INTER_CUBIC)
        # cv2.imshow('iker', res)
        # cv2.imshow('image', image)
        cv2.waitKey(0)
        # cv2.destoryAllWindows()
        cv2.imwrite('../static/images/80%s.png' %(img), res, [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

    # # 放大图像
    # fx = 1.6
    # fy = 1.2
    # enlarge = cv2.resize(img, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

    # # 显示
    # cv2.imshow("src", img)
    # cv2.imshow("shrink", shrink)
    # cv2.imshow("enlarge", enlarge)
    #
    cv2.waitKey(0)