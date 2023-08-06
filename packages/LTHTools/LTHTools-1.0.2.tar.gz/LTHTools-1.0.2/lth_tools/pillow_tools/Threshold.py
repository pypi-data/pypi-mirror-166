# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     Threshold
   Description :   
   Author :       lth
   date：          2022/8/30
-------------------------------------------------
   Change Activity:
                   2022/8/30 17:08: create this script
-------------------------------------------------
"""
__author__ = 'lth'

from PIL import Image


class Threshold:
    def __init__(self, threshold=200):
        self.table = []
        for i in range(256):
            if i < threshold:
                self.table.append(0)
            else:
                self.table.append(1)

    def process(self, img):
        img = img.convert("L")

        img = img.point(self.table, '1')
        return img.convert("RGB")


if __name__ == "__main__":
    path = "C:/Users/lth/Desktop/real_data/zhaoshang/105,179.13.jpg"

    image = Image.open(path)
    model = Threshold()
    image = model.process(image)
    image.show()
