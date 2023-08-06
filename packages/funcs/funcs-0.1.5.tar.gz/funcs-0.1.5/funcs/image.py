import numpy as np
from PIL import Image


def read_image(path: str) -> np.ndarray:
    """ Reads an image in RGB format and returns it as a numpy array.

    Args:
        path (str): path to image

    Returns:
        image: numpy array in RGB format
    """
    image = Image.open(path)
    image = image.convert('RGB')
    return np.array(image)
