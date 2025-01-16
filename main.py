import json
from time import sleep

import setting
from xiaomi.XiaoMi import XiaoMiNote
from vivo.Vivo import VivoNote


# 用于将本地vivo原子笔记备份，上传到小米便签中
def start():
    # 获取vivo笔记列表，暂时只获取1页，一页500条
    vivoNote = VivoNote()
    vivoList = vivoNote.getNoteList()
    # 列表最后10个元素，然后逆序
    for index, item in enumerate(vivoList[-2:][::-1]):  # 正序[0:15]    [78:131]    [::-1]列表逆序
        content = ''.join(item.get('content'))  # 笔记列表转成字符串
        title = item.get('title')
        xiaoMiNote = XiaoMiNote(headers=setting.xiaomi.get('headers'),
                                content=content, title=title)
        xiaoMiNote.createNote()
        # 需要添加创建时间，创建时间为createTime
        xiaoMiNote.saveNote(addTime=setting.addTime, createTime=item.get('createtime'),
                            updateTime=item.get('updatedate'))
        print('==================成功添加第{}条==================='.format(index))
        # sleep(1)


if __name__ == '__main__':
    start()
