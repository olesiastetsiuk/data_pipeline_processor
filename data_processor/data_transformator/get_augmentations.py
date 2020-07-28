import os

import numpy as np
import cv2
from matplotlib import pyplot as plt
from skimage.color import label2rgb

import random

import albumentations as A

from albumentations import (
    RandomCrop, HorizontalFlip, IAAPerspective, ShiftScaleRotate, CLAHE, RandomRotate90,
    Transpose, ShiftScaleRotate, Blur, OpticalDistortion, GridDistortion, HueSaturationValue,
    IAAAdditiveGaussianNoise, GaussNoise, MotionBlur, MedianBlur, IAAPiecewiseAffine,
    IAASharpen, IAAEmboss, RandomBrightnessContrast, Flip, OneOf, Compose
)

BOX_COLOR = (255, 0, 0) # Red
TEXT_COLOR = (255, 255, 255) # White

def augment_and_show(aug, image, filename=None, 
                     font_scale_orig=0.35, font_scale_aug=0.35, **kwargs):

    augmented = aug(image=image)

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_aug = cv2.cvtColor(augmented['image'], cv2.COLOR_BGR2RGB) 
    
    f, ax = plt.subplots(1, 2, figsize=(16, 8))
    
    ax[0].imshow(image)
    ax[0].set_title('Original image')
    
    ax[1].imshow(image_aug)
    ax[1].set_title('Augmented image')
    
    f.tight_layout()

    if filename is not None:
        f.savefig(filename)
        
    return augmented['image']

def crop_transformation(image, percent_of_height, percent_of_width):

    h, w, c = image.shape

    crop = A.Compose([
    RandomCrop(h*percent_of_height, w*percent_of_width, always_apply=True, p=1.0)], p=1)
    result = augment_and_show(crop, image)
    return result


def resize_transformation(image, height, width):

    resize = A.Compose([Resize(height, width, interpolation=1, always_apply=False, p=1)], p=1)
    result = augment_and_show(resize, image)
    return result







