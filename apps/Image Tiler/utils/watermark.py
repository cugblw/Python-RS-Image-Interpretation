# -*- encoding: utf-8 -*-

'''
@File    :   watermark.py
@Time    :   2022/06/26 09:45:01
@Author  :   Weil Lee
@Version :   1.0
@Email   :   cugblw2014@outlook.com
@Desc    :   None
'''


import random
from PIL import Image
from PIL import ImageDraw, ImageFont,ImageEnhance


def generate_watermark_by_image(img):
    """
    Generate watermark image
    """
    # logo_path = 'src/static/images/cennavi_logo.png'
    logo_path = 'core/images/cennavi_logo.png'
    watermark = Image.open(logo_path)
    logo_width, logo_height = watermark.size
    
    # Image width and height
    width, height = img.size
    
    margin = 5
    x = width - logo_width - margin
    y = height - logo_height - margin

    img.paste(watermark, (random.randint(0,x), random.randint(0,y)), watermark)
    
    return img

def generate_watermark_by_text(img):
    """
    Generate watermark image by text
    """
    #Image width and height
    logo_text = 'Image Tiler@Lee'
    width, height = img.size
    text = logo_text
    font = ImageFont.truetype('arial.ttf', 15)
    draw = ImageDraw.Draw(img,"RGBA")
    
    textwidth, textheight = draw.textsize(text, font)

    margin = 5
    x = random.randint(0, (width - margin - textwidth)) #center
    y = random.randint(0, (height - margin - textheight )) #center
    draw.text((x, y), text, font=font, fill = (255,255,255,150))

    return img