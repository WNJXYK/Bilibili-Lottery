# Bilibili-Lottery
这是一个有点花哨的 Bilibili 抽奖程序，从评论用户中抽取（排序）若干名幸运观众。（支持筛选粉丝 / 弹幕）


运行环境: Python 3.x

依赖包: numpy, matplotlib, tkinter, requests

使用方法：
* 在 `cookie.txt` 中填入账号的 Cookie 信息
* 运行 `Lottery.py`
* 填入视频 av 号，并点击 `Set Video AV`
* 点击 `Get Users`，获取评论 & 弹幕用户
* 设置筛选条件，点击 `Lottery`
