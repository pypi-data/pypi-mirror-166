# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     StyleTransferLoss
   Description :   
   Author :       lth
   date：          2022/9/6
-------------------------------------------------
   Change Activity:
                   2022/9/6 16:31: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import torch.nn.functional as F
from torch import nn

from ..utils import gram_matrix


class ContentLoss(nn.Module):
    def __init__(self, reduction="mean"):
        super(ContentLoss, self).__init__()
        self.reduction = reduction

    def forward(self, input_tensor, target):
        return F.l1_loss(input_tensor, target, reduction=self.reduction)


class StyleLoss(nn.Module):
    def __init__(self, reduction="mean"):
        super(StyleLoss, self).__init__()
        self.reduction = reduction

    def forward(self, input_tensor, target):
        gram_input = gram_matrix(input_tensor)
        gram_target = gram_input(target)
        return F.l1_loss(gram_input, gram_target, reduction=self.reduction)
