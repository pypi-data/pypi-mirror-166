# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     Upsample
   Description :   
   Author :       lth
   date：          2022/9/2
-------------------------------------------------
   Change Activity:
                   2022/9/2 10:59: create this script
                   还在修改的过程中
-------------------------------------------------
"""
__author__ = 'lth'

import torch
from torch import nn
from torch.autograd import Function


class Upsample2d_(Function):
    @staticmethod
    def forward(ctx, input: torch.Tensor, scale_size):
        ctx.save_for_backward(input,scale_size)
        new_input = input.repeat(1,1,1,scale_size[1]).repeat(1,1,scale_size[0],1)

        return new_input

    @staticmethod
    def backward(ctx, grad_outputs):
        result,scale_size = ctx.saved_tensors
        grad = grad_outputs[:, :, :scale_size[0], ::scale_size[1]]
        return result*grad,None,None


class Upsamle2d(nn.Module):
    def __init__(self, scale_size):
        super(Upsamle2d, self).__init__()

        self.size = torch.tensor(scale_size)

    def forward(self, x):
        return Upsample2d_.apply(x, self.size)

if __name__=="__main__":
    model = Upsamle2d(scale_size=(2,2))
    dummy_input = torch.randn([1,1,2,2],requires_grad=True)
    print(dummy_input)
    output = model(dummy_input)
    print(output)
    loss =torch.mean(output)
    loss.backward()