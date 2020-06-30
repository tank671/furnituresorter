import numpy as np
import torch
from torch import nn

class MyAdaptiveConcatPool2d(nn.Module):
    "Layer that concatenates `AdaptiveAvgPool2d` and `AdaptiveMaxPool2d`"
    # modified from fastai2
    def __init__(self, size=None):
        super().__init__()
        self.size = size or 1
        self.ap = nn.AdaptiveAvgPool2d(self.size)
        self.mp = nn.AdaptiveMaxPool2d(self.size)
    def forward(self, x): return torch.cat([self.mp(x), self.ap(x)], 1)

def _get_norm(prefix, nf, ndim=2, zero=False, **kwargs):
    "Norm layer with `nf` features and `ndim` initialized depending on `norm_type`."
    # from fastai2
    assert 1 <= ndim <= 3
    bn = getattr(nn, f"{prefix}{ndim}d")(nf, **kwargs)
    if bn.affine:
        bn.bias.data.fill_(1e-3)
        bn.weight.data.fill_(0. if zero else 1.)
    return bn

def myBatchNorm(nf, ndim=2, **kwargs):
    "BatchNorm layer with `nf` features and `ndim` initialized depending on `norm_type`."
    # from fastai2
    return _get_norm('BatchNorm', nf, ndim, zero=False, **kwargs)

class myLinBnDrop(nn.Sequential):
    "Module grouping `BatchNorm1d`, `Dropout` and `Linear` layers"
    # modified from fastai2
    def __init__(self, n_in, n_out, bn=True, p=0., act=None, lin_first=False):
        layers = [myBatchNorm(n_out if lin_first else n_in, ndim=1)] if bn else []
        if p != 0: layers.append(nn.Dropout(p))
        lin = [nn.Linear(n_in, n_out, bias=not bn)]
        if act is not None: lin.append(act)
        layers = lin+layers if lin_first else layers+lin
        super().__init__(*layers)

def my_create_head():
    # modified from fastai2
    lin_ftrs = [4096, 512, 8]
    ps = [0.5/2] * ( len(lin_ftrs)-2) + [0.5]
    activations = [nn.ReLU(inplace=True)] * (len(lin_ftrs)-2) + [None]
    pool = MyAdaptiveConcatPool2d()
    layers = [pool, nn.Flatten()]
    for ni,no,p,actn in zip(lin_ftrs[:-1], lin_ftrs[1:], ps, activations):
        layers += myLinBnDrop(ni, no, bn=True, p=p, act=actn, lin_first=False)
    return nn.Sequential(*layers)

