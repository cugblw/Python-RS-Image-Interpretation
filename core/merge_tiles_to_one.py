import math
# from tkinter.tix import 
from PIL import Image

def getImageFilePath(file_path, x, y, zoom):
    return file_path + "/" +  str(zoom) + "_" + str(x) + '_'+ str(y)+'.jpg'

def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)

def resize_image(img, size):
    img_new = img.resize((size, size), Image.BOX)
    return img_new

def mergeAllImageToOne(file_path, zoom, params):
    xmin = params[0]
    ymin = params[1]
    xmax = params[2]
    ymax = params[3]
    mw = 256 
    toImage = Image.new('RGB', (256*(xmax-xmin), 256*(ymax-ymin)) )

    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
        
            fname = getImageFilePath(file_path, x, y, zoom)
            fromImage = Image.open(fname)
            fromImage = fromImage.convert('RGB')
            # draw = ImageDraw.Draw(fromImage)
            
            # # 添加每个瓦片的文字信息
            # fontSize = 18
            # setFont = ImageFont.truetype('C:/windows/fonts/arial.ttf', fontSize)
            # fillColor = "#ffff00"
            # pos = num2deg(x, y, zoom)
            # text = 'Tile: ' + str(x)+ "," + str(y)+ "," + str(zoom)
            # text2 = 'Lat: %.6f'%pos[0]
            # text3 = 'Lon: %.6f'%pos[1]
            # draw.text((1,1), text,font=setFont,fill=fillColor)
            # draw.text((1,1+fontSize), text2,font=setFont,fill=fillColor)
            # draw.text((1,1+2*fontSize), text3,font=setFont,fill=fillColor)
            
            # # 添加每个瓦片的边框线条
            # draw.rectangle([0, 0, mw-1, mw-1], fill=None, outline='red', width=1)
            
            # 将每个瓦片的小图绘制到大图里面。
            toImage.paste(fromImage, ((x-xmin) * mw, (y-ymin) * mw))

    image_new = resize_image(toImage, 256)
    toImage.save(file_path + '/merge.jpg' )
    image_new.save(file_path + '/merge_resize.jpg' )
    toImage.close()

if __name__ == '__main__':
    file_path = r'C:\Users\Administrator\Desktop\tile_move\satellite\16\R12\C25'
    mergeAllImageToOne(file_path, 16, [51636, 25707, 51645, 25717])
    # 51636, 51645, 25707, 25717