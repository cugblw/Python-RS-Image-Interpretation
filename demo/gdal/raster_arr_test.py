from PIL import Image
import numpy as np

sub_array = np.arange(16).reshape((4,4))

big_array = np.zeros((10,10))


print(sub_array)
# print(big_array)
big_array[3:7,5:9] = sub_array
print(big_array.shape)
print(sub_array.shape)

print(sub_array.shape == big_array)

arr = np.arange(10).reshape((5,2))
# row:height , col:width 
print(arr.shape)


height = 12000
width  = 5000


def get_resize_times(height,width,size):
    times_height = height/(size*20)
    times_width = width/(size*20)
    times = max(times_height,times_width)

    return times
print(get_resize_times(12000,5000,512))

if (int(height/512) > 20) or (int(width/512)>20):
    height_new = int(height/get_resize_times(height, width, 512))
    width_new = int(width/get_resize_times(height, width, 512))
    print(height_new,width_new)

def resize_image_by_times(img,times):
    width,height = img.size
    img_new = img.resize((int(width/times),int(height/times)))
    return img_new
    

img = Image.open(r"E:\Coding\Python\Python-RS-Image-Interpretation\test_resize.png")

img_new = resize_image_by_times(img, get_resize_times(12000,5000,512) )

print(img.size)
print(img_new.size)
data = np.array
img_empty = np.zeros(shape=(height,width))

# img_new.save("test_resize_by_times.png")

a = 6

if 0 <= a <10:
    print(a)