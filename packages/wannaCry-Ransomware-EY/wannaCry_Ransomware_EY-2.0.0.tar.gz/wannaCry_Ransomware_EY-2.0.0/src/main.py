import os
from src.include import im_innocent
from pathlib import Path
from PIL import Image, UnidentifiedImageError


def convert(image: str) -> int and str or None:
    try:
        if not os.path.exists(image):
            raise FileNotFoundError(f"image {image} was NOT found!")
        im = Image.open(image)
        image_path = Path(image).parent
        image_name = Path(image).stem
        out_image = os.path.join(image_path, image_name + ".jpg")
        rgb_im = im.convert('RGB')
        rgb_im.save(out_image)
        print("Saved as " + out_image)
        return 0, out_image
    except (FileNotFoundError, PermissionError,
            UnidentifiedImageError, AttributeError, TypeError) as e:
        print(e)
        return 1, None
