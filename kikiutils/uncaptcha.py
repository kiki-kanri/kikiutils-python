import cv2 as _cv2
import io as _io
import multiprocessing as _multiprocessing
import numpy as _numpy

from PIL import Image as _Image

from .check import isfile as _isfile, isstr as _isstr
from .image import cmp_image_sim as _cmp_image_sim, get_image as _get_image


class Dun360:
    def __init__(
        self,
        bg_image: _Image.Image | _io.BytesIO | _io.FileIO | bytes | str,
        slide_image: _Image.Image | _io.BytesIO | _io.FileIO | bytes | str,
        multiprocessing_use_cpu: int = _multiprocessing.cpu_count(),
        use_multiprocessing: bool = True
    ):
        if _isstr(bg_image):
            if not _isfile(bg_image):
                bg_image = _get_image(bg_image)

        if _isstr(slide_image):
            if not _isfile(slide_image):
                slide_image = _get_image(slide_image)

        if not getattr(bg_image, 'convert', False):
            bg_image = _Image.open(bg_image).convert('RGB')

        if not getattr(slide_image, 'convert', False):
            slide_image = _Image.open(slide_image, formats=['png'])

        self.bg_image = bg_image
        self.slide_image = slide_image
        self.mp_use_cpu = multiprocessing_use_cpu
        self.use_mp = use_multiprocessing

    def crop_bg_and_cmp_slide_image(
        self,
        bg_image: _Image.Image,
        slide_dst_image: _cv2.Mat,
        dx: int,
        w2: int,
        h2: int
    ):
        crop_image = bg_image.crop((dx, 0, dx + w2, h2))
        crop_cv2_image = _cv2.cvtColor(
            _numpy.array(crop_image), _cv2.COLOR_RGB2GRAY)
        crop_dst_image = _cv2.Canny(crop_cv2_image, 100, 200)
        pasted_image = _cv2.add(crop_dst_image, slide_dst_image)
        sim_value = _cmp_image_sim(
            crop_dst_image, pasted_image, resize_image=False)

        return {
            sim_value: dx
        }

    def get_slide_move_x(self):
        bg_image = self.bg_image.copy()
        slide_image = self.slide_image.copy()

        W1, H1 = bg_image.size
        W2, H2 = slide_image.size

        # Change slide image pixel is transparent to 0, 0, 0, 0 (RGBA)
        # If pixel is not transparent, change to 255, 255, 255, 255 (RGBA)

        for w in range(W2):
            for h in range(H2):
                R, G, B, A = slide_image.getpixel((w, h))

                if R == G == 255 or A == 0:
                    slide_image.putpixel((w, h), (0, 0, 0, 0))
                else:
                    slide_image.putpixel((w, h), (255, 255, 255, 255))

        # Get slide image bbox position and crop
        box__pos = slide_image.getbbox()
        box__pos = (box__pos[0] - 5, box__pos[1] - 5,
                    box__pos[2] + 5, box__pos[3] + 5)
        bg_image = bg_image.crop((0, box__pos[1], W1, box__pos[3]))
        slide_image = slide_image.crop(box__pos)

        # Get resized bg and slide image width and height
        W1, H1 = bg_image.size
        W2, H2 = slide_image.size

        # Use cv2.Canny to process croped slide image
        slide_cv2_image = _cv2.cvtColor(
            _numpy.array(slide_image), _cv2.COLOR_RGB2GRAY)
        slide_dst_image = _cv2.Canny(slide_cv2_image, 100, 200)
        sim_results = {}

        # Crop bg image and add slide dst image, then cmp crop and pasted image hash
        if self.use_mp:
            pool = _multiprocessing.Pool(self.mp_use_cpu)
            args = []

            for dx in range(W1 - W2):
                args.append((bg_image, slide_dst_image, dx, W2, H2))

            result = pool.starmap(self.crop_bg_and_cmp_slide_image, args)
            pool.close()
            pool.join()

            # Get max sim value and dx
            for r in result:
                sim_results.update(r)
        else:
            for dx in range(W1 - W2):
                r = self.crop_bg_and_cmp_slide_image(
                    bg_image, slide_dst_image, dx, W2, H2)
                sim_results.update(r)

        sim_list = list(sim_results.keys())
        sim_list.sort()

        max_sim_value = sim_list[-1]
        max_sim_dx = sim_results[max_sim_value] + 5

        return {
            'max_sim': max_sim_value,
            'max_sim_dx': max_sim_dx
        }
