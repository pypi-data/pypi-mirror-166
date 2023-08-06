# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     FocalLoss
   Description :   
   Author :       lth
   date：          2022/8/30
-------------------------------------------------
   Change Activity:
                   2022/8/30 15:46: create this script
-------------------------------------------------
"""
__author__ = 'lth'

import torch

from ..utils import clamp


class FocalLoss(torch.nn.Module):
    def __init__(self, alpha=1, beta=1, eps=1e-5, reduction="sum"):
        super(FocalLoss, self).__init__()
        assert reduction in ["sum", "mean", "none"]
        self.reduction = reduction
        self.eps = eps
        self.alpha = alpha
        self.beta = beta

    def calculate_BCE_version(self, input_tensor, target=None):
        input_tensor = clamp(input_tensor, self.eps)

        output = -self.alpha * (1 - input_tensor) ** self.beta * torch.log(input_tensor) * target - self.alpha * (
            input_tensor) ** self.beta * torch.log(1 - input_tensor) * target

        if self.reduction is "sum":
            output = torch.sum(output)
        elif self.reduction is "mean":
            output = torch.mean(output)
        elif self.reduction is "none":
            pass
        else:
            raise ValueError("reduction must be sum , mean , none")

        return output

    def calculate_CrossEntropy_version(self, input_tensor, target):
        input_tensor = clamp(input_tensor, self.eps)
        output = - self.alpha * (1 - input_tensor) ** self.beta * torch.log(1 - input_tensor) * target

        if self.reduction is "sum":
            output = torch.sum(output)
        elif self.reduction is "mean":
            output = torch.mean(output)
        elif self.reduction is "none":
            pass
        else:
            raise ValueError("reduction must be sum , mean , none")

        return output
