import os
import mimetypes
from typing import Iterable
from pathlib import Path

import torch
from torchvision import models
from PIL import Image
from PIL.Image import BILINEAR
from torchvision.transforms import ToTensor, Normalize


imagenet_stats = ([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
image_extensions = set(k for k, v in mimetypes.types_map.items() if v.startswith('image/'))
totensor = ToTensor()
normalize = Normalize(*imagenet_stats)
CATEGORIES = ['bookshelf', 'cabinet', 'console', 'details', 'door', 'railing', 'table', 'vase']

def listify(o):
    # from fastai course v3p2
    # https://github.com/fastai/course-v3/blob/master/nbs/dl2/04_callbacks.ipynb
    if o is None: return []
    if isinstance(o, list): return o
    if isinstance(o, str): return [o]
    if isinstance(o, Iterable): return list(o)
    return [o]

def setify(o):
    # from fastai course v3p2
    # https://github.com/fastai/course-v3/blob/master/nbs/dl2/08_data_block.ipynb
    if isinstance(o, set):
        return o
    else:
        return listify(o)

def _get_files(path, files, extensions=None):
    # from fastai course v3p2
    # https://github.com/fastai/course-v3/blob/master/nbs/dl2/08_data_block.ipynb
    path = Path(path)
    res = [path/f for f in files if not f.startswith('.')
           and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)]
    return res

def get_files(path, extensions=None, recurse=False, include=None, exclude=None):
    # modified from fastai course v3p2
    # https://github.com/fastai/course-v3/blob/master/nbs/dl2/08_data_block.ipynb
    # TODO: add functionality to exclude folders (will be used for 'auto_' folders)
    path = Path(path)
    extensions = setify(extensions)
    extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i,(p,d,f) in enumerate(os.walk(path)): # returns (dirpath, dirnames, filenames)
            if include is not None and i==0: d[:] = [o for o in d if o in include]
            else:                            d[:] = [o for o in d if not o.startswith('.')]
            res += _get_files(p, f, extensions)
        return res
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        return _get_files(path, f, extensions)

def load_image(filename, mode='RGB', **kwargs):
    # modified from fastai2.vision.core
    # from PIL import Image
    im = Image.open(filename, **kwargs)
    im.load()
    im = im._new(im.im)
    if mode:
        return im.convert(mode)
    else:
        return im

def prepare_image(filename):
    im = load_image(filename).resize((256, 256), resample=BILINEAR)
    im = normalize(totensor(im)).unsqueeze(0)
    return im

def create_folders(output_folder):
    for cat in CATEGORIES:
        new_folder = os.path.join(output_folder, f"auto_{cat}")
        print(new_folder)
        Path(new_folder).mkdir(parents=True, exist_ok=True) #this part is fine, just commenting out for now