import os
import random
from PIL import Image


# watermark = Image.open('watermark_logo.png')

img_dir = "C:/Users/Administrator/Desktop/watermarktest"
img_list = os.listdir( img_dir )
watermark = Image.open('cennavi.png')
logo_width, logo_height = watermark.size


for img in img_list:
    if os.path.isfile(img_dir + '/' + img):
        #Create an Image Object from an Image
        im = Image.open(img_dir + '/' + img)
        #Image name
        img_name = os.path.basename(img)
        
        #Image width and height
        width, height = im.size

        margin = 5
        x = width - logo_width - margin
        y = height - logo_height - margin

        im.paste(watermark, (random.randint(0,x), random.randint(0,y)), watermark)
        img_name = os.path.basename("watermark_logo_" + img_name)

        #Save watermarked image
        im.save('images/' + img_name)