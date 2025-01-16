import datetime
import time

import requests
import json


# 小米笔记 包含创建和保存
class XiaoMiNote:
    noteId = ''
    serviceToken = ''
    headers = {}
    # 创建时间,初始化的时候不传入默认当前时间，传入了则使用传入时间--->后经测试，不可用，传入了时间，接口创建出出来的还是会使用当前时间
    createDate = ''
    # vivo笔记内容
    content = ''
    title = ''

    def __init__(self, headers=None, content=None, title=None):
        if (headers is None) or (content is None) or (title is None):
            raise Exception('serviceToken、headers、content或者title未传入')
        # 从cookie中提取serviceToken
        cookie = headers['Cookie']
        # 按";"分割字符串，得到一个列表
        parts = cookie.split(";")
        # 遍历列表，找到包含"serviceToken="的元素
        for part in parts:
            if "serviceToken=" in part:
                # 按"="分割，取第二个元素即为serviceToken的值
                self.serviceToken = part.split("=")[1]
                break
        self.headers = headers
        self.content = content
        self.title = title
        self.createDate = int(datetime.datetime.now().timestamp() * 1000)
        print('小米类初始化完成')

    def now(self):
        return int(datetime.datetime.now().timestamp() * 1000)

    def createNote(self):

        obj = {"content": "", "colorId": 0, "folderId": "0", "createDate": self.createDate, "modifyDate": self.now()}
        kw = {
            'entry': json.dumps(obj),
            "serviceToken": self.serviceToken
        }
        # 发送请求 创建笔记
        res = requests.post("https://i.mi.com/note/note", data=kw, headers=self.headers)
        if res.status_code != 200:
            raise Exception('创建小米笔记请求失败，状态码：' + str(res.status_code))
        data = json.loads(res.text)
        self.noteId = str(data.get('data').get('entry').get('id'))
        print('小米创建笔记完成')

    def setContent(self, content):
        self.content = content

    def setTitle(self, title):
        self.title = title

    def saveNote(self, addTime=True, createTime=None, updateTime=None):
        createTimeStr = ''

        # 如果vivo笔记存在创建和更新时间，则在小米笔记下方记录
        if updateTime:
            # 换行再加上更新时间
            createTimeStr += '\n<text indent=\"1\"></text>\n<text indent=\"1\"><u><background color=\"#4139ff\"><b><i>更新时间：{}</i></b></background></u></text>'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(int(updateTime) / 1000))))

        if createTime:
            # 不换行加上创建时间
            createTimeStr += '\n<text indent=\"1\"><u><background color=\"#9affe8af\"><b><i>创建时间：{}</i></b></background></u></text>'.format(
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(int(createTime) / 1000))))

        # 将vivo笔记内容转换为小米笔记，待办事项那里
        self.convertNote()

        print(self.content+createTimeStr)
        # 保存笔记
        obj = {
            "id": self.noteId,
            "tag": self.noteId,
            "status": "normal",
            "createDate": self.createDate,
            "modifyDate": self.now(),
            "colorId": 0,
            "folderId": "0",
            "alertDate": 0,
            "extraInfo": {"title": self.title},
            "content": self.content + createTimeStr if (addTime and createTimeStr != '') else self.content
        }

        kw2 = {
            'entry': json.dumps(obj),
            "serviceToken": self.serviceToken
        }
        # https://i.mi.com/note/note/38151228775875424
        url = "https://i.mi.com/note/note/" + self.noteId
        res = requests.post(url, data=kw2, headers=self.headers)
        if res.status_code != 200:
            raise Exception('保存小米笔记请求失败，状态码：' + str(res.status_code))
        data = json.loads(res.text)
        print('小米保存笔记完成')

    def convertNote(self):
        if self.content:
            tempStr = str(self.content)
            # 替换笔记中待完成事项和已完成事项图标
            newStr = tempStr.replace('[ ]', '<input type=\"checkbox\" indent=\"1\" level=\"3\" />')\
                .replace('[x]', '<input type=\"checkbox\" indent=\"1\" level=\"3\" checked=\"true\" />')
            self.content = newStr


# 测试vivo笔记格式转换为小米笔记格式
def testConvertNote():
    xiaoMiNote = XiaoMiNote(headers='',
                            content='<p>转专业</p><p>大一成绩占15℅</p><p>考试高数和英语占60℅</p><p>专业考试占25℅◐c语言和面试◑</p>',
                            title='')
    xiaoMiNote.convertNote()
    print(str(xiaoMiNote.content))


if __name__ == '__main__':
    testConvertNote()
