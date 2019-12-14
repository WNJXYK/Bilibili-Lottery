# Bilibili-Lottery
这是一个有点花哨的 Bilibili 抽奖程序，从评论用户中抽取（排序）若干名幸运观众。（支持筛选粉丝 / 弹幕）

### 环境
运行环境: Python 3.x

依赖包: numpy, matplotlib, tkinter, requests

### 使用方法
* 在 `cookie.txt` 中填入账号的 Cookie 信息
* 运行 `Lottery.py`
* 填入视频 av 号，并点击 `Set Video AV`
* 点击 `Get Users`，获取评论 & 弹幕用户
* 设置筛选条件，点击 `Lottery`

### 常见问题
Q1: 图标中文无法现实

A1: Matplot 的中文现实问题，见 `Lottery.py` 第 8 行，填入系统有的中文字体即可

Q2: 模拟什么过程？

A2: 理想的社会财富随机流动过程，n 个人初始持有一定金币，每一回合每个人随机将自己的一枚金币给 n 个人中的一个人（可能自己），随机进行若干回合。

