import os
import torch

from shutil import copy2
from pathlib import Path
from torch import nn
from torchvision import models
from furnituresorter.utils import prepare_image, CATEGORIES
from furnituresorter.layers import my_create_head

def classify(pictures, output_folder=None):

    my_head = my_create_head()
    my_body = nn.Sequential(*list(models.resnet50().children())[:8])
    model = nn.Sequential(my_body, my_head).eval()
    weights = torch.load('app\\resources\\weights.pth', map_location='cpu')
    model.load_state_dict(weights) 
    
    for p in pictures:
        predicted_category = CATEGORIES[torch.argmax(model(prepare_image(p)))]
        print(predicted_category)
        dest = os.path.join(output_folder, Path("auto_{}".format(predicted_category)))
        copy2(p, dest) # copy2 attempts to preserve metadata