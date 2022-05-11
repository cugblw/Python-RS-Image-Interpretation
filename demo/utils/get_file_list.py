import os 

# method 1 os.walk实现
def get_tile_list1(path):
    tar_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            if file.endswith(".tar"):
                print(os.path.join(root, file))
                tar_list.append(file)
                tar_file_path = os.path.join(root, file)
                print(tar_file_path)

    # print(tar_list)

# method 2 os.listdir实现
def get_tile_list2(path):
    file_list = os.listdir(path)
    for file in file_list:
        print(file)


if __name__ == '__main__':
    path = r'E:\satellite\data_result\5MjdiCKeDLht\satellite\10'
    get_tile_list1(path)

