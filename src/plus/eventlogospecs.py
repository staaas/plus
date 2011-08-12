from imagekit.specs import ImageSpec
from imagekit import processors

class ResizePosterDisplay(processors.Resize):
    width = 300

class PosterDisplay(ImageSpec):
    quality = 75  # defaults to 70
    increment_count = True
    processors = [ResizePosterDisplay]
