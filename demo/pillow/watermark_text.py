import os, sys
import random
from PIL import Image, ImageDraw, ImageFont

img_dir = "images/"
dirs = os.listdir( img_dir )

for img in dirs:
	if os.path.isfile(img_dir + img):
		#Create an Image Object from an Image
		im = Image.open(img_dir + img)
		
		#Image width and height
		width, height = im.size
		
		#Image name
		img_name = os.path.basename(img_dir + "watermark_text_" + img)
		
		#print(img_name)

		text = "@2022 Cennavi"
		font = ImageFont.truetype('arial.ttf', 15)
		
		draw = ImageDraw.Draw(im,"RGBA")
		
		textwidth, textheight = draw.textsize(text, font)

		margin = 5

		x = random.randint(0, (width - margin - textwidth)) #center
		y = random.randint(0, (height - margin - textheight )) #center
		
		draw.text((x, y), text, font=font, fill = "red")
		#im.show() //Will display in the image window
		
		#Save watermarked image
		im.save('images/' + img_name)