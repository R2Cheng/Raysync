

def decode_permission(permission):
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
    if permission !=0:
        st = bin(permission).split()[0]
    else:
        st = "00000000000000"
    permission_list = []
    for i in st:
        permission_list.append(i)
    admin_permission = {
        "list": False,
        "upload":False,
        "download":False,
        "mkdir":False,
        "rename":False,
        "remove":False,
        "copy":False,
        "move":False,
        "share":False,
        "invite":False
    }
    if permission_list[3] == "1":
        admin_permission["list"] = True
    if permission_list[4] == "1":
        admin_permission["download"] = True
    if permission_list[6] == "1":
        admin_permission["remove"] = True
    if permission_list[7] == "1":
        admin_permission["rename"] = True
    if permission_list[8] == "1":
        admin_permission["mkdir"] = True
    if permission_list[9] == "1":
        admin_permission["upload"] = True
    if permission_list[10] == "1":
        admin_permission["move"] = True
    if permission_list[11] == "1":
        admin_permission["copy"] = True
    if permission_list[12] == "1":
        admin_permission["share"] = True
    if permission_list[13] == "1":
        admin_permission["invite"] = True

    return admin_permission
data = decode_permission(4095)
print(data)