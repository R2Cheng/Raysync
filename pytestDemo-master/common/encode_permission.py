data = "abcdefghijkl"
"""
2-CWD:1
3-List:2
4-retr:4  #下载
5-appe:8
6-dele:16
7-rnfr:32 #重命名
8-mkd:64  #创建文件夹
9-stor:128 #上传
10-move:256
11-copy:512
12-share:1024
13-invite:2048
"""
import itertools
def permission_combine():
    a = []
    data= ["CWD","List","retr","appe","dele","rnfr","mkd","stor","move","copy","share","invite"]
    for i in range(0,len(data)):
        for j in itertools.combinations(data, i):
            a.append(j)
    return a

def decode_permission_1():
    data = permission_combine()
    permission = []
    for permission_list in data:
        CWD, List, retr, appe, dele, rnfr, mkd, stor, move, copy, share, invite = "0","0","0","0","0","0","0","0","0","0","0","0"
        for i in permission_list:
            if i == "CWD":
                CWD = "1"
            if i == "List":
                List = "1"
            if i == "retr":
                retr = "1"
            if i == "appe":
                appe = "1"
            if i == "dele":
                dele = "1"
            if i == "rnfr":
                rnfr = "1"
            if i == "mkd":
                mkd = "1"
            if i == "stor":
                stor = "1"
            if i == "move":
                move = "1"
            if i == "copy":
                copy = "1"
            if i == "share":
                share = "1"
            if i == "invite":
                invite = "1"
        all_persission = CWD+List+retr+appe+dele+rnfr+mkd+stor+move+copy+share+invite
        all_persission = int(all_persission,2)
        permission.append(all_persission)
    return permission


a = decode_permission_1()
print(a)