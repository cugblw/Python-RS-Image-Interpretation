from hashlib import new
import re
from PIL import Image, ImageFilter
import numpy as np


def composite_ocean_color():
    image = Image.open("res/image/16_51688_25727.jpg")
    # image.show()
    # image = image.filter(ImageFilter.GaussianBlur(radius=10))
    image_blur = image.filter(ImageFilter.BoxBlur(radius=50))
    image.show()
    # image_blur = image.filter(ImageFilter.GaussianBlur(radius=10))

    new_image = Image.new("RGBA", image.size,"#131D29")
    new_image.paste(image, (0,0),image)
    new_image.convert("RGB")
    # new_image.show()

    Image.fromarray(np.hstack((np.array(image),np.array(new_image)))).show()


def create_oceanic_image():
    size = (256, 256)
    image = Image.new("RGB", size,"#131D29")
    # image.show()
    return image

def create_blank_image():
    size = (256, 256)
    image = Image.new("RGB", size,"#131D29")
    return image
    

if __name__ == "__main__":
    create_oceanic_image()