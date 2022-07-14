import os
import time

import imageio.v2 as imageio


def sort_date (date_list):
    '''
    :param list_of_dates:
    :return:
    '''
    date_list= ['2022-07-13', '2022-07-12', '2022-07-11', '2022-07-10', '2022-07-09', '2022-07-08', '2022-07-07', '2022-07-06', '2022-07-05', '2022-07-04', '2022-07-03', '2022-07-02', '2022-07-01', '2022-06-30']
    date_list.sort(key=lambda x: time.mktime(time.strptime(x,"%Y-%m-%d")))
    return date_list


def create_gif(image_list, gif_name, fps = 2):
    '''
    :param image_list: 这个列表用于存放生成动图的图片
    :param gif_name: 字符串，所生成gif文件名，带.gif后缀
    :param fps: 帧率，即每秒显示多少帧
    :return:
    ''' 
    frames = []
    # sort the image list by date
    image_list.sort(key = lambda x: time.mktime(time.strptime(x.split('/')[-1].split("_")[-1].split('.')[0],"%Y-%m-%d")))
    for image_name in image_list:
        frames.append(imageio.imread(image_name))

    imageio.mimsave(gif_name, frames, fps=fps)
    return

if __name__ == '__main__':
    image_dir = r'C:\Users\Administrator\Desktop\gif'
    image_list = []
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith('.jpg'):
                image_list.append(os.path.join(root, file).replace("\\","/"))
    gif_name = r'C:\Users\Administrator\Desktop\gif\test.gif'
    create_gif(image_list, gif_name)