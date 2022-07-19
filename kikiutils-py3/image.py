import cv2 as _cv2
import io as _io
import numpy as _numpy

from PIL import Image as _Image
from typing import Union

from .check import isbytes as _isbytes, response_is_ok as _response_is_ok
from .file import get_file_mime as _get_file_mime
from .file import save_file as _save_file
from .file import save_file_as_bytesio as _save_file_as_bytesio
from .requests import get_response as _get_response


_Image.MAX_IMAGE_PIXELS = None


# Image

def convert_image(
    image_file: Union[bytes, _io.BytesIO, _io.FileIO],
    format: str = 'webp',
    quality: int = 100,
    get_bytes: bool = False
):
    """Convert image to other format, return bytes or BytesIO object."""

    try:
        if _isbytes(image_file):
            image_file = _io.BytesIO(image_file)
        image = _Image.open(image_file)

        return _save_file_as_bytesio(
            image.save,
            get_bytes,
            format=format,
            quality=quality,
            lossless=False
        )
    except:
        return False


def cmp_image_dhash(dhash1, dhash2):
    """Compare two image dhash."""

    n = 0

    if len(dhash1) != len(dhash2):
        raise ValueError('Image dhash length mismatch!')

    for i in range(len(dhash1)):
        if dhash1[i] != dhash2[i]:
            n += 1

    return n


def cmp_image_sim(
    image1: _cv2.Mat,
    image2: _cv2.Mat,
    resize_image: bool = True
):
    """Compare two image similarity.

    Images must be of the same size and type.
    """

    image1_dhash = get_image_dhash(image1, resize_image)
    image2_dhash = get_image_dhash(image2, resize_image)

    cmp_dhash = cmp_image_dhash(image1_dhash, image2_dhash)
    return 1 / (cmp_dhash or 1)


def download_image(
    url: str,
    save_path: str,
    max_size: int = 5242880,
    save_format: str = 'webp'
):
    """Get and convert image by url then save.

    If you want to get bytes, use `get_image` method.
    """

    response = _get_response(url)

    if _response_is_ok(response, False):
        image_bytes = response.content

        if len(image_bytes) <= max_size:
            return save_image(image_bytes, save_path, save_format)

    return False


def get_image(
    url: str,
    check: bool = True,
    get_bytes: bool = False
) -> _io.BytesIO:
    """Get image by url, return bytes or BytesIO object."""

    response = _get_response(url)

    if _response_is_ok(response, False):
        image_bytes = response.content

        if check:
            image_mime = _get_file_mime(image_bytes)

            if image_mime[0] != 'image':
                return False

        if get_bytes:
            return image_bytes
        return _io.BytesIO(image_bytes)


def get_image_dhash(image: Union[_cv2.Mat, _numpy.ndarray], resize: bool = True):
    """Get image dhash."""

    if resize:
        while True:
            h, w = image.shape[0], image.shape[1]

            if h <= 128 or w <= 128:
                break

            image = _cv2.resize(image, (int(w / 2), int(h / 2)))

    h, w = image.shape[0], image.shape[1]
    hash_str = ''

    for i in range(h):
        for j in range(w - 1):
            hash_str = hash_str + \
                ('1' if image[i, j] > image[i, j + 1] else '0')

    return hash_str


def save_image(
    image_file: Union[bytes, _io.BytesIO, _io.FileIO],
    save_path: str,
    format: str = 'webp',
    image_mime: list = None
):
    """Save image."""

    if image_file:
        if getattr(image_file, 'read', None):
            image_file = image_file.read()
        if not image_mime:
            image_mime = _get_file_mime(image_file)

        if image_mime[0] == 'image':
            if image_mime[1] != format:
                image_file = convert_image(
                    image_file, format, return_bytes=True)

            return _save_file(image_file, save_path)

    return False
