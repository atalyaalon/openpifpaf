"""Transform input data.

Images are resized with Pillow which has a different coordinate convention:
https://pillow.readthedocs.io/en/3.3.x/handbook/concepts.html#coordinate-system

> The Python Imaging Library uses a Cartesian pixel coordinate system,
  with (0,0) in the upper left corner. Note that the coordinates refer to
  the implied pixel corners; the centre of a pixel addressed as (0, 0)
  actually lies at (0.5, 0.5).
"""
import os

import torchvision

from .annotations import AnnotationJitter, NormalizeAnnotations
from .compose import Compose
from .crop import Crop
from .hflip import HFlip
from .image import Blur, ImageTransform, JpegCompression
from .minsize import MinSize
from .multi_scale import MultiScale
from .pad import CenterPad, CenterPadTight, SquarePad
from .preprocess import Preprocess
from .random import DeterministicEqualChoice, RandomApply
from .rotate import RotateBy90
from .scale import RescaleAbsolute, RescaleRelative, ScaleMix
from .unclipped import UnclippedArea, UnclippedSides


EVAL_TRANSFORM = Compose([
    NormalizeAnnotations(),
    ImageTransform(torchvision.transforms.ToTensor()),
    ImageTransform(
        torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                         std=[0.229, 0.224, 0.225]),
    ),
])

def get_train_transform(add_noise=False, blur_max_sigma=5):
    if add_noise:
        TRAIN_TRANSFORM = Compose([
            NormalizeAnnotations(),
            ImageTransform(torchvision.transforms.ColorJitter(
                brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1)),
            RandomApply(JpegCompression(), 0.1),  # maybe irrelevant for COCO, but good for others
            RandomApply(Blur(max_sigma=blur_max_sigma), 0.5),  # maybe irrelevant for COCO, but good for others
            ImageTransform(torchvision.transforms.RandomGrayscale(p=0.01)),
            EVAL_TRANSFORM,
        ])
    else:
        TRAIN_TRANSFORM = Compose([
            NormalizeAnnotations(),
            ImageTransform(torchvision.transforms.ColorJitter(
                brightness=0.1, contrast=0.1, saturation=0.1, hue=0.1)),
            RandomApply(JpegCompression(), 0.1),  # maybe irrelevant for COCO, but good for others
            # RandomApply(Blur(), 0.01),  # maybe irrelevant for COCO, but good for others
            EVAL_TRANSFORM,
        ])
    return TRAIN_TRANSFORM
