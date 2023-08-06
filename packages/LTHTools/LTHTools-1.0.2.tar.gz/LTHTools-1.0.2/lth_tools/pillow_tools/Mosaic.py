# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     Mosaic
   Description :   
   Author :       lth
   date：          2022/9/6
-------------------------------------------------
   Change Activity:
                   2022/9/6 16:46: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import random

import numpy as np
from PIL import Image


class Mosaic:
    def __init__(self, image_size=None):
        if image_size is None:
            image_size = [800, 1024]
        self.image_size = image_size

    def __call__(self, images, boxes):
        """
        images: [image,...]
        boxes:[box,...]
        """
        assert len(images) == len(boxes), "the length of images and boxes should be same"
        assert len(images) <= 4, "default length should less than 4"
        target_image = Image.new("RGB", self.image_size, (128, 128, 128))
        target_box = []
        #                x                                                   y
        start_points = [[0 + random.randint(0, 15), 0 + random.randint(0, 15)],
                        [self.image_size[0] // 2 + random.randint(-15, 15), 0 + random.randint(0, 15)],
                        [0 + random.randint(0, 15), self.image_size[1] // 2 + random.randint(-15, 15)],
                        [self.image_size[0] // 2 + random.randint(-15, 15),
                         self.image_size[1] // 2 + random.randint(-15, 15)]]
        for i in range(len(images)):
            img = images[i]
            b = boxes[i]
            img, b = self.standard_image_process(img, b)
            img, b = self.process_image(img, b)

            if i == 0:
                target_image.paste(img, tuple(start_points[i]))
                b[:, [0, 2]] += start_points[i][0]
                b[:, [1, 3]] += start_points[i][1]
                target_box.append(b)
            elif i == 1:
                target_image.paste(img, tuple(start_points[i]))
                b = self.process_paste(target_box, b, start_points[i], i)
                target_box.append(b)
            elif i == 2:
                target_image.paste(img, tuple(start_points[i]))
                b = self.process_paste(target_box, b, start_points[i], i)
                target_box.append(b)
            elif i == 3:
                target_image.paste(img, tuple(start_points[i]))
                b = self.process_paste(target_box, b, start_points[i], i)
                target_box.append(b)
            else:
                pass

        target_box = np.concatenate(target_box)

        target_box[target_box[:, 3] > self.image_size[1], 3] = self.image_size[1]
        target_box[target_box[:, 2] > self.image_size[0], 2] = self.image_size[0]

        return target_image, target_box

    @staticmethod
    def process_image(img, b):
        width, height = img.width, img.height
        scale = random.uniform(0.65, 0.75)
        img = img.resize((int(width * scale), int(height * scale)))
        b[:, [0, 2]] = b[:, [0, 2]] * scale
        b[:, [1, 3]] = b[:, [1, 3]] * scale
        return img, b

    def standard_image_process(self, img, b):
        width, height = img.width, img.height
        ratio = (width / height)

        if ratio > 1:
            nw = self.image_size[0]
            nh = int(self.image_size[1] / ratio)
        else:
            nh = self.image_size[0]
            nw = int(self.image_size[1] * ratio)

        img = img.resize((nw, nh))
        b[:, [0, 2]] = b[:, [0, 2]] * (nw / width)
        b[:, [1, 3]] = b[:, [1, 3]] * (nh / height)
        return img, b

    @staticmethod
    def process_paste(target_box, b, start_point, index):
        """
        index 0 1 2 3
        """

        # Shear
        if index == 1:
            assert len(target_box) == 1, "should be equal to 1"
            # x1 过滤
            # x2 裁剪
            target_box[0] = target_box[0][target_box[0][:, 0] < start_point[0]]
            target_box[0][target_box[0][:, 2] >= start_point[0], 2] = int(start_point[0])
        elif index == 2:
            assert len(target_box) == 2, "should be equal to 2"
            # y1 过滤
            # y2 裁剪
            target_box[0] = target_box[0][target_box[0][:, 1] < start_point[1]]
            target_box[0][target_box[0][:, 3] >= start_point[1], 3] = int(start_point[1])

            target_box[1] = target_box[1][target_box[1][:, 1] < start_point[1]]
            target_box[1][target_box[1][:, 3] >= start_point[1], 3] = int(start_point[1])

        elif index == 3:
            assert len(target_box) == 3, "should be equal to 3"
            # x1 过滤
            # x2 裁剪

            target_box[0] = target_box[0][target_box[0][:, 0] < start_point[0]]
            target_box[0][target_box[0][:, 2] >= start_point[0], 2] = int(start_point[0])

            target_box[2] = target_box[2][target_box[2][:, 0] < start_point[0]]
            target_box[2][target_box[2][:, 2] >= start_point[0], 2] = int(start_point[0])

            # y1 过滤
            # y2 裁剪
            target_box[0] = target_box[0][target_box[0][:, 1] < start_point[1]]
            target_box[0][target_box[0][:, 3] >= start_point[1], 3] = int(start_point[1])

            target_box[1] = target_box[1][target_box[1][:, 1] < start_point[1]]
            target_box[1][target_box[1][:, 3] >= start_point[1], 3] = int(start_point[1])

        b[:, 0] = b[:, 0] + start_point[0]
        b[:, 2] = b[:, 2] + start_point[0]
        b[:, 1] = b[:, 1] + start_point[1]
        b[:, 3] = b[:, 3] + start_point[1]

        return b


if __name__ == "__main__":

    def get_boxes(label_route):
        lines = open(label_route, "r", encoding="utf-8").readlines()
        boxes = " ".join(lines)
        return boxes.split()


    import os

    path = "C:/Users/HP/Desktop/yolov5data/customs/images/val/"
    images = []
    boxes = []
    for root, dir, files in os.walk(path):
        for file in files:
            images.append(os.path.join(root, file))

    for image in images:
        label = image.replace("images", "labels").replace(".jpg", ".txt")
        line_label = get_boxes(label)
        line_label = list(map(float, line_label))
        box = []
        image = Image.open(image).convert("RGB")
        h, w = image.height, image.width

        for i in range(0, len(line_label), 5):
            b = line_label[i:i + 5]
            box.append(
                #           x1                  y1                      x2                    y2
                [(b[1] - b[3] / 2) * w, (b[2] - b[4] / 2) * h, (b[1] + b[3] / 2) * w, (b[2] + b[4] / 2) * h, b[0]])
        box = sorted(box, key=lambda x: -(x[2] - x[0]) * (x[3] - x[1]))
        box = np.array(box, dtype=np.float)
        boxes.append(box)

    images = images[:4]
    boxes = boxes[:4]

    model = Mosaic()

    pil_image = []
    for img in images:
        pil_image.append(Image.open(img).convert("RGB"))

    target_image, target_box = model(pil_image, boxes)
    from PIL.ImageDraw import ImageDraw

    image_draw = ImageDraw(target_image)
    for b in target_box:
        image_draw.rectangle((b[0], b[1], b[2], b[3]), outline="red", width=2)

    target_image.show()
