# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     utils
   Description :   
   Author :       lth
   date：          2022/8/30
-------------------------------------------------
   Change Activity:
                   2022/8/30 15:48: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import torch


def clamp(input_tensor, eps):
    """
    将数值做夹逼裁剪，防止loss计算中的log溢出

    :param input_tensor: torch.tensor
    :param eps: 1e-5
    :return: torch.tensor
    """
    input_tensor = torch.clamp(input_tensor, eps, 1 - eps)
    return input_tensor


def minmaxScale(input_tensor):
    """
    将数值做归一化处理

    :param input_tensor: torch.tensor
    :return: torch.tensor
    """
    min_ = torch.min(input_tensor)
    max_ = torch.max(input_tensor)
    input_tensor = (input_tensor - min_) / (max_ - min_)
    return input_tensor


def gram_matrix(input_tensor):
    """
    gram矩阵操作 可以用于风格迁移 和 细粒度分类

    :param input_tensor:torch.tensor
    :return:torch.tensor
    """
    a, b, c, d = input_tensor.size()
    features = input_tensor.view(a * b, c * d)
    G = torch.mm(features, features.t())
    return G.div(a * b * c * d)


def denormalize(im, mean=0.5, std=0.5):
    """
    图片反标准化操作

    :param im: Union[np.ndarray, torch.Tensor]
    :param mean: float
    :param std:float
    :return:Union[np.ndarray, torch.Tensor]
    """
    return im * std + mean
