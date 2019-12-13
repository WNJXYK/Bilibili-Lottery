from tkinter import Tk, Entry, Button, Frame, Listbox, IntVar, Label, END, Checkbutton
from Bilibili_Dev import BDev
import numpy as np
import matplotlib.pyplot as plt

# Variable

root = Tk()
root.title('Bilibili Lottery')

bdev = BDev(debug=False)
oid_arr = []
comment_arr, dm_arr = {}, {}
player_arr, lottery_arr, name_arr =[], {}, {}
fans_opt, dm_opt = IntVar(), IntVar()

# Frame Layout
setting_frame = Frame(root)
setting_frame.pack(side="left")
game_frame = Frame(root)
game_frame.pack(side="top")
data_frame = Frame(root)
data_frame.pack(side="right")

# Game Logic
def play(max_iter = 100, n_disp = 50):
    global player_arr, lottery_arr, name_arr, comment_arr, dm_arr, fans_opt, dm_opt
    player_arr, lottery_arr, name_arr =[], {}, {}

    for mid in comment_arr:
        if fans_opt.get() == 1 and (not comment_arr[mid][1]): continue
        if dm_opt.get() == 1 and (mid not in dm_arr): continue
        player_arr.append(mid)
        lottery_arr[mid] = 10
        name_arr[mid] = comment_arr[mid][0]

    player_arr = np.array(player_arr)
    n = player_arr.shape[0]
    n_disp = min(n_disp, n)
    np.random.shuffle(player_arr)

    plt.ion()
    for iter in range(max_iter):
        # Gift
        gift = np.random.choice(np.arange(n), size=n, replace=True)
        for i in range(n):
            cur, nxt = player_arr[i], player_arr[gift[i]]
            if lottery_arr[cur] == 0: continue
            lottery_arr[cur] -= 1
            lottery_arr[nxt] += 1

        # Gen Plot
        rnk_arr = sorted(player_arr, key=lambda x: lottery_arr[x], reverse=True)
        x, y = [], []
        for i in range(n_disp):
            x.append(name_arr[rnk_arr[i]])
            y.append(lottery_arr[rnk_arr[i]])

        # Update Plot
        plt.rcParams['font.sans-serif'] = ['Songti SC']
        plt.barh(range(n_disp), y, tick_label=x, color="y")
        plt.title("Step %d / %d" % (iter + 1, max_iter))
        plt.xlabel("Show Top %d of %d" % (n_disp, n))
        plt.show()
        plt.pause(0.001)

        # Clear / Show Result
        if iter + 1 < max_iter:
            plt.clf()
        else:
            res_root = Tk()
            res_root.title('Bilibili Lottery Result')
            res_list = Listbox(res_root, listvariable=None)
            res_list.pack()

            fp = open("result.txt", "w")
            for i in range(n):
                res_list.insert(END, "%d: %s - %d" % (rnk_arr[i], name_arr[rnk_arr[i]], lottery_arr[rnk_arr[i]]))
                fp.write("%d: %s - %d\n" % (rnk_arr[i], name_arr[rnk_arr[i]], lottery_arr[rnk_arr[i]]))
            fp.close()

            res_root.mainloop()

# Setting Logic
aid_label = Label(setting_frame, text="Video AV", font=('Arial', 16))
aid_input = Entry(setting_frame, show=None)
oid_list = Listbox(setting_frame, listvariable=None)
oid_label = Label(setting_frame, text="Video List", font=('Arial', 16))
set_label = Label(setting_frame, text="Lottery Options", font=('Arial', 16))
com_check = Label(setting_frame, text="✔️Sent a comment!", font=('Arial', 13))
fan_check = Checkbutton(setting_frame, text='Be your fans!',variable=fans_opt, onvalue=1, offvalue=0)
dm_check = Checkbutton(setting_frame, text='Sent a DM!',variable=dm_opt, onvalue=1, offvalue=0)

def set_video_aid():
    global aid, oid_arr, bdev
    aid = aid_input.get()
    oid_arr = bdev.get_videos(aid)
    oid_list.delete(0, END)
    for oid in oid_arr: oid_list.insert(END, oid)

set_aid = Button(setting_frame, text='Set Video AV', font=('Arial', 16), command=set_video_aid)
lottery = Button(setting_frame, text='Lottery', font=('Arial', 16), command=play)


# Data Logic
comment_label = Label(data_frame, text="Comments", font=('Arial', 16))
comment_list = Listbox(data_frame, listvariable=None)
dm_label = Label(data_frame, text="DM", font=('Arial', 16))
dm_list = Listbox(data_frame, listvariable=None)

def get_video_info():
    global aid, oid_arr, comment_arr, dm_arr, bdev
    comment_arr = bdev.get_comments_user(aid)
    dm_arr = {}
    for oid in oid_arr:
        dm_arr.update(bdev.get_dm_user(oid))
    comment_list.delete(0, END)
    dm_list.delete(0, END)
    for mid in comment_arr:
        comment_list.insert(END, "%s%s(%d) " % ("*" if comment_arr[mid][1] else "", comment_arr[mid][0], mid))
    for mid in dm_arr:
        dm_list.insert(END, "%s(%d)" % (dm_arr[mid][0], mid))

get_info = Button(setting_frame, text='Get Info', font=('Arial', 16), command=get_video_info)

# Setting Frame
aid_label.pack()
aid_input.pack()
set_aid.pack()
oid_label.pack()
oid_list.pack()
get_info.pack()
set_label.pack()
com_check.pack()
fan_check.pack()
dm_check.pack()
lottery.pack()


# Data Frame
comment_label.pack()
comment_list.pack()
dm_label.pack()
dm_list.pack()

# Start Main Window
root.mainloop()

# 77657890