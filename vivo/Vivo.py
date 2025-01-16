import os
import glob

import setting


class VivoNote:
    # {'id': 5444185850, 'title': '测试笔记转换',
    #                   'thumb': 'https://fenghuang-prd-bj.vivo.com.cn/cloud-file-encrypt/cloud/encrypt/684bf7ec6d12fa343b0ce994f1f06d24.jpg?AccessKeyId=CwcQysjYD8QPiqqiqC2G&Expires=1737030812&Signature=sgiTDoj7qL5C6SwsftlnB%2B5P7eQ%3D',
    #                   'folderName': '便签', 'check': 2, 'createtime': '1635813403232', 'updatedate': 1737011423448,
    #                   'hasRecord': 0, 'hasAlarm': 0, 'timeForTopSort': 4890611423476, 'isStickTop': 1}
    VivoDatas = []

    def __init__(self):
        print('a')

    def getNoteList(self):
        # 指定文件夹路径
        folder_path = setting.notesPath  # 请将这里的路径替换为你的目标文件夹路径

        # 检查文件夹是否存在
        if not os.path.exists(folder_path):
            print(f"文件夹 {folder_path} 不存在")
        else:
            # 使用glob模块匹配所有.txt文件
            txt_files = glob.glob(os.path.join(folder_path, '*.txt'))

            # 获取每个文件的修改时间，并与文件路径一起存储在列表中
            files_with_mtime = [(file_path, os.path.getmtime(file_path)) for file_path in txt_files]

            # txt文件按修改时间升序排序
            files_with_mtime.sort(key=lambda x: x[1], reverse=False)

            # 遍历排序后的文件列表
            for index, (file_path, mtime) in enumerate(files_with_mtime, start=1):
                print(f"文件: {index}个, 路径: {file_path}, 修改时间: {mtime}")
                # 可以在这里添加对文件的进一步处理，例如读取文件内容等
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.readlines()  # 读取所有行，返回一个列表
                    # 判断第一行是否有数据，没有数据则该文件没有title
                    if content and content[0].strip():
                        # 获取不带扩展名的文件名
                        file_name = os.path.splitext(os.path.basename(file_path))[0]
                        title = file_name
                    else:
                        title = ''
                    # 注意：使用export.js脚本会多两行，这里删除
                    # 判断笔记是否有题目，删除content的前两行
                    if content:
                        content = content[2:]

                    # 插入字典元素到列表中
                    self.VivoDatas.append({
                        'title': title,
                        'content': content,
                    })
            return self.VivoDatas
