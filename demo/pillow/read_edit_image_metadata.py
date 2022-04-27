from hashlib import new
from exif import Image

img_path = "E:/Coding/Python/Python-RS-Image-Interpretation/test_resize.jpg"
# img_path = "E:/Coding/Python/Python-RS-Image-Interpretation/14_12223_7048.png"

with open(img_path, 'rb') as img_file:
    img = Image(img_file)

print(img.has_exif)

# List all EXIF tags contained in the image
print(sorted(img.list_all()))

img.copyright = 'Kenneth Leung 2021'
print(f'Copyright: {img.get("copyright")}')
img.artist = "weil"
print(f'artist: {img.get("artist")}')

img.software = 'Pillow'
print(f'software: {img.get("software")}')

with open(img_path, 'wb') as new_image_file:
        new_image_file.write(img.get_file())