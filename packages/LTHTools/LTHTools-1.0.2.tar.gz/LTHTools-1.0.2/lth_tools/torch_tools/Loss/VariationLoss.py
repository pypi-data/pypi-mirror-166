# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     VariationLoss
   Description :   
   Author :       lth
   date：          2022/9/6
-------------------------------------------------
   Change Activity:
                   2022/9/6 14:52: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import torch
from torch import nn

'''
保证图片在行和列上面的变化比较正常，没有出现断裂
'''


class VariationLoss(nn.Module):
    """
    该loss可以使图像变得平滑,降噪
    """
    def __init__(self, k_size: int) -> None:
        super(VariationLoss, self).__init__()
        self.k_size = k_size

    def forward(self, input_tensor: torch.Tensor):
        n, c, h, w = input_tensor.shape
        tv_h = torch.mean(torch.pow(input_tensor[:, :, self.k_size:, :] - input_tensor[:, :, :-self.k_size, :], 2))
        tv_w = torch.mean(torch.pow((input_tensor[:, :, :, self.k_size:] - input_tensor[:, :, :, :-self.k_size]), 2))
        tv_loss = (tv_w + tv_h) / (c * h * w)
        return tv_loss
