import requests, json


class BDev:
    def __init__(self, debug=False):
        '''
        初始化 Bilibili API 模块
        用户的 Cookie 存储在同目录 cookie.txt 文件夹中
        :param debug: 是否输出中间信息
        '''

        # Init
        self.debug = debug

        # Read Cookie
        try:
            fp = open("cookie.txt", "r")
            self.cookie = fp.readline()
            if self.debug: print(self.cookie)
        except Exception as e:
            raise Exception("Bilibili-Dev - Cannot read cookie in cookie.txt. Error : %s" % str(e))

        # Check User
        mid, msg = self.check_user()
        if mid is None:
            raise Exception("Bilibili-Dev - Invalid cookie. Message : %s" % msg)
        else:
            print(" * Bilibili-Dev : Welcome User %d." % mid)

        # self.get_comments_user(77657890)
        # for oid in self.get_videos(77657890):
        #     self.get_dm_user(oid)

    def check_user(self):
        '''
        检查用户 Cookie 是否有效
        :return: 用户 mid，错误信息（当用户 mid 为 None 时错误）
        '''
        url = "https://member.bilibili.com/x/web/elec/user"
        code, text = self.get(url, {})
        ret = json.loads(text)
        if self.debug: print(ret)

        if ret["code"] == 0:
            return ret["data"]["mid"], ""

        return None, ret["message"]

    def get_comments_user(self, aid):
        '''
        获取视频的评论用户信息
        :param aid: 视频 av 号
        :return: 字典：用户 mid -> (昵称, 是否关注, )
        '''
        user = {}

        def render_user(arr):
            for item in arr["data"]:
                id, nick, fans = item["mid"], item["replier"], (item["relation"] == 2)
                if id not in user:
                    user[id] = (nick, fans, )

        n_items = 50
        arr = self.get_comments_raw(aid, ps=n_items)
        n_pages = int((arr["pager"]["total"] + n_items - 1) / n_items)
        render_user(arr)
        print(" * Bilibili-Dev : Comments pages %d / %d" % (1, n_pages))

        for cur_pages in range(2, n_pages + 1):
            print(" * Bilibili-Dev : Comments pages %d / %d" % (cur_pages, n_pages))
            arr = self.get_comments_raw(aid, ps=n_items, pn=cur_pages)
            render_user(arr)

        if self.debug: print(user)

        return user

    def get_comments_raw(self, aid, pn=1, ps=50):
        '''
        获取视频评论的原始信息
        :param aid: 视频 av 号
        :param pn: 当前页数，从 1 开始
        :param ps: 每页多少条
        :return: 原始 JSON 信息
        '''
        url = "https://member.bilibili.com/x/web/replies"
        params = {
            "type": 1,
            "oid": aid,
            "ps": ps,
            "pn": pn
        }
        code, text = self.get(url, params)
        ret = json.loads(text)
        if self.debug: print(ret)

        if ret["code"] != 0: raise Exception("Bilibili-Dev - Invalid parameters for getting comments. Message : %s" % ret["message"])

        return ret

    def get_dm_user(self, oid):
        '''
        获取发送弹幕的用户信息
        :param oid: 分 P 的编号
        :return: 字典：用户 mid -> (用户昵称, )
        '''
        user = {}

        def render_user(arr):
            if arr["data"]["result"] is None: return
            for item in arr["data"]["result"]:
                id, nick = item["mid"], item["uname"]
                if id not in user: user[id] = (nick, )

        n_items = 50
        arr = self.get_dm_raw(oid, ps=n_items)
        n_pages = int((arr["data"]["page"]["total"] + n_items - 1) / n_items)
        render_user(arr)
        print(" * Bilibili-Dev : DM pages 1 / %d" % n_pages)

        for i in range(2, n_pages + 1):
            print(" * Bilibili-Dev : DM pages %d / %d" % (i, n_pages))
            render_user(self.get_dm_raw(oid, ps=n_items, pn=i))

        if self.debug: print(user)

        return user

    def get_videos(self, aid):
        '''
        获取一个视频的所有分 P 编号
        :param aid: 视频 av 号
        :return: 分 P 编号列表
        '''
        url = "https://member.bilibili.com/x/web/archive/parts"
        params = { "aid": aid }
        code, text = self.get(url, params)

        ret = json.loads(text)
        if self.debug: print(ret)

        if ret["code"] != 0: raise Exception(
            "Bilibili-Dev - Invalid parameters for getting videos. Message : %s" % ret["message"])

        res = []
        for item in ret["data"]["part_list"]:
            res.append(item["cid"])

        if self.debug: print(res)

        return res

    def get_dm_raw(self, oid, pn=1, ps=50):
        '''
        获取视频弹幕的原始数据
        :param oid: 分 P 编号
        :param pn: 当前页数
        :param ps: 每页多少条信息
        :return: JSON 原始数据
        '''
        url = "https://api.bilibili.com/x/v2/dm/search"
        params = {
            "type": 1,
            "oid": oid,
            "ps": ps,
            "pn": pn,
            "type": 1
        }
        code, text = self.get(url, params)
        ret = json.loads(text)
        if self.debug: print(ret)

        if ret["code"] != 0: raise Exception(
            "Bilibili-Dev - Invalid parameters for getting dm. Message : %s" % ret["message"])

        return ret

    def get(self, url, params):
        '''
        模拟 GET 请求
        :param url: 网站
        :param params: 参数
        :return: 状态号, 数据
        '''
        headers = {
            "Accept": "*/*",
            "Accept - Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cookie": self.cookie,
            "Origin": "https: // member.bilibili.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        }

        response = requests.get(
            url,
            params=params,
            headers=headers
        )

        return response.status_code, response.text

# BDev(debug=True)