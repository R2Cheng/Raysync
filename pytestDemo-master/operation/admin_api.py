from core.result_base import ResultBase
from api.user import raysync
from common.logger import logger
from common.encry_hash import hashids_encode
import time

def admin_login(admin_user,admin_passwd):
    # 登录
    data = {
        "UK": hashids_encode(admin_user) + hashids_encode(admin_passwd),
        "action": "login",
        "device": "",
        "id": int(time.time()),
        "module": "WEBADMIN",
        "token": None,
        "version": "3.0.3.2"}
    respone = raysync.raysync_request(json=data)
    return respone

def selectAdmin(token):
    #查看admin账户
    selectAdmin_data = {
        "action":"SELECT_ADMIN",
        "adminId":1,
        "device":"",
        "id":int(time.time()),
        "module":"WEBADMIN",
        "token":token,
        "version":"3.0.3.2"
    }
    respone = raysync.raysync_request(json=selectAdmin_data)
    return respone

def admin_logout(token):
    #登出
    logout_data = {"action": "logout",
                  "module": "WEBADMIN",
                  "device": "",
                  "id": int(time.time()),
                  "token": token,
                  "version": "3.0.3.2"}
    respone = raysync.raysync_request(json=logout_data)
    return respone
def admin_updateadmin(token,admin,oldpasswd,newpasswd):
    #更新当前管理员信息
    try:
        updataadmin_data = {"action": "UPDATE_ADMIN",
                          "adminId": 1,
                          "module": "WEBADMIN",
                          "device": "",
                          "id": int(time.time()),
                          "newAccount":  admin,
                          "newPassword": hashids_encode(newpasswd),
                          "oldPassword": hashids_encode(oldpasswd),
                          "token": token,
                          "version": "3.0.3.2"}

        respone = raysync.raysync_request(json=updataadmin_data)
        return respone
    except Exception as e:
        logger.exception("更新当前管理员信息出现错误，错误是{}".format(e))

def admin_upadteserver(token,name,host,proxyPort,packageSize,outbounde,compression,license):
    #更新服务器信息
    try:
        updataserver_data = {
                            "server":{
                                "id":1000,
                                "name": name, #服务器名称
                                "host": host, #服务器地址 支持域名和IP地址
                                "proxyPort": proxyPort, #UDP加速端口
                                "packageSize": packageSize, #UDP报文大小 600 ~ 1442
                                "outbound": outbounde*1024*1024, #出口带宽 Mbps 设置0或不填，带宽限制不生效
                                "compression": compression,#启用压缩  0为不压缩
                                "license":license, #激活码

                                "device": "",
                                "enableFTPS": True,
                                "inbound": 104857600,
                                "version": "3.0.2.8"
                            },
                            "action":"UPDATE_SERVER",
                            "id":int(time.time()),
                            "version":"3.0.3.2",
                            "device":"",
                            "module":"WEBADMIN",
                            "token":token
                        }
        respone = raysync.raysync_request(json=updataserver_data)
        return respone
    except Exception as e:
        logger.exception("更新服务器信息，错误是{}".format(e))

def admin_createuser(token,account,passwd,name="",needUpdatePwd=1,email="",home="",exclude_list=[],permission=4095,uploadSpeed=0,downloadSpeed=0,syncSwitch=False,
                     uploadSuffixLimit=0,suffixList=[],emailSenderType=0,whitelistIPSwitch=False,whitelistIP="",groupIdList=[]):
    #新建用户
    try:
        createuser_data = {"action": "CREATE_USER",
                          "module": "WEBADMIN",
                          "device": "",
                          "user": {
                               "name": name,#姓名
                               "account": account,#账号
                               "password": hashids_encode(passwd),#密码
                               "needUpdatePwd": needUpdatePwd,#是否强制用户首次登录时修改密码
                               "email": email,#邮箱
                               "home": home,#主目录
                               "exclude_list":exclude_list,#禁止访问路径
                               "permission": permission,#权限
                               "uploadSpeed": int(uploadSpeed * 1024 * 1024 / 8),   #上传速度限制
                               "downloadSpeed": int(downloadSpeed * 1024 * 1024 / 8),#下载速度限制
                               "syncSwitch": syncSwitch,#同步目录功能
                               "address": "",
                               "uploadSuffixLimit": uploadSuffixLimit,	# 文件格式白名单 0：不开启限制，1：开启白名单限制
                               "suffixList": suffixList,	# 文件后缀列表，传入数组
                               "emailSenderType": emailSenderType, #邮件发送方 0：以管理员配置邮箱发送  1：以用户配置邮箱发送
                               "whitelistIPSwitch" : whitelistIPSwitch ,#IP登录白名单  0：不开启限制  1：开启限制
                               "whitelistIP" : whitelistIP, #IP白名单限制列表，传入字符串
                                "company": "",
                               "accountType": 2,#1：管理员 2：普通用户 3：分享用户 4：ad域用户 5：邮箱用户  6：unix系统用户
                               "created": 0,
                            "phone": "",
                            "remark": "",
                            "status": 0,
                              "authWay": "",
                              "groupIdList":""
                        },
                          "groupIdList" : groupIdList, #关联用户组
                          "id": int(time.time()),
                          "token": token,
                          "version": "3.0.3.2"}
        respone = raysync.raysync_request(json=createuser_data)
        return respone
    except Exception as e:
        logger.exception("新建用户，错误是{}".format(e))

def setUserHomeCountPeriod(token,time):
    #空间统计
    try:
        setUserHomeCountPeriod_data = {
            "action":"SET_USER_HOME_COUNT_PERIOD",
            "data":{"period":time * 60 * 60},
            "device":"",
            "module":"WEBADMIN",
            "token":token,
            "version":"3.0.3.2"
        }
        respone = raysync.raysync_request(json=setUserHomeCountPeriod_data)
        return respone
    except Exception as e:
        logger.exception("空间统计，错误是{}".format(e))

def resetFileList():
    #logo设置
    try:
        resetFileList_data = {
            "action":"RESET_FILE_LIST",
            "data":[],
            "device":"",
            "id":int(time.time()),
            "is_bg_change":False,
            "is_icon_change":False,
            "is_logo_change":False,
            "module":"WEBADMIN",
            "token":"DQeRzYGZxWidrvEXOs3qg5N0kPbALWmJuFsS0hjE",
            "version":"3.0.3.2"
        }
        respone = raysync.raysync_request(json=resetFileList_data)
        return respone
    except Exception as e:
        logger.exception("logo设置，错误是{}".format(e))

def setLogo():
    #logo设置
    try:
        setlogo_data = {
            "token":"DQeRzYGZxWidrvEXOs3qg5N0kPbALWmJuFsS0hjE",
            "logo":"C:\\Users\\linsijie\\Downloads\\1.jpg",
            "background":"C:\\Users\\linsijie\\Downloads\\2.jpg",
            "ico":"C:\\Users\\linsijie\\Downloads\\3.jpg"
        }
        headers = {"Content-Type":"multipart/form-data",
                   "Connection":"keep-alive"}
        respone = raysync.raysync_request_setlogo(data=setlogo_data,headers=headers)
        return respone
    except Exception as e:
        logger.exception("logo设置，错误是{}".format(e))


def addNotice(token,title,content,userNotice,emailLanguage):
    addNotice_data = {
        "action":"ADD_NOTICE",
        "data":{
            "content":content,
            "emailLanguage":emailLanguage,
            "userNotice":userNotice,
            "title":title
        },
        "device":"",
        "id":int(time.time()),
        "token": token,
        "version": "3.0.3.2"
    }
    response = raysync.raysync_request(json=addNotice_data)
    return response

def sessions(token):
    # 获取实时传输列表
    try:
        sessions_data = {
            "action": "sessions",
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "version": "3.0.3.2"
        }
        response = raysync.raysync_request(json=sessions_data)
        return response
    except Exception as e:
        logger.exception("获取实时传输列表，错误是{}".format(e))

def stopTask(token,task_name):
    #暂停正在传输的任务
    try:
        stopTask_data = {
            "action": "STOP_TASK",
            "data":{
                "task_name":task_name
            },
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "version": "3.0.3.2"
        }
        response = raysync.raysync_request(json=stopTask_data)
        return response
    except Exception as e:
        logger.exception("暂停正在传输的任务，错误是{}".format(e))
def getAllShareLink(token,stime,etime,type=0):
    #获取邀请上传和分享下载列表
    try:
        getAllShareLink_data = {
            "accountType":0,
            "action":"GET_ALL_SHARELINK",
            "count":10,
            "device": "",
            # "getShareList": 0,
            "id": int(time.time()),
            "module": "WEBADMIN",
            "order": 1,
            "orderBy": 2,
            "page": 1,
            # "query": "",
            "selectEndTime": int(time.mktime(time.strptime(str(etime),"%Y-%m-%d %H:%M:%S" ))),
            "selectShareStatus": 0,
            "selectStartTime": int(time.mktime(time.strptime(str(stime),"%Y-%m-%d %H:%M:%S"))),
            "selectUserId": 0,
            "token": token,
            "type": type,
            "version": "3.0.3.2"
        }
        response = raysync.raysync_request(json=getAllShareLink_data)
        return response
    except Exception as e:
        logger.exception("获取邀请上传和分享下载列表，错误是{}".format(e))

def delShareLink(token,url):
    #删除链接
    try:
        delShareLink_data = {
            "action": "DEL_SHARELINK",
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "url":url,
            "version": "3.0.3.2"
        }
        response = raysync.raysync_request(json=delShareLink_data)
        return response
    except Exception as e:
        logger.exception("删除链接，错误是{}".format(e))

def disableShareLink(token,url):
    #取消邀请上传和分享下载链接
    try:
        disableShareLink_data = {
            "action": "DISABLE_SHARELINK",
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "url": url,
            "version": "3.0.3.2",
        }
        response = raysync.raysync_request(json=disableShareLink_data)
        return response
    except Exception as e:
        logger.exception("取消邀请上传和分享下载链接，错误是{}".format(e))

def admin_createuser(token,account,passwd,name="",needUpdatePwd=1,email="",home="",exclude_list=[],permission=4095,uploadSpeed=0,downloadSpeed=0,syncSwitch=False,
                         uploadSuffixLimit=0,suffixList=[],emailSenderType=0,whitelistIPSwitch=False,whitelistIP="",groupIdList=[]):
    #新建用户
    try:
        createuser_data = {"action": "CREATE_USER",
                          "module": "WEBADMIN",
                          "device": "",
                          "user": {
                               "name": name,#姓名
                               "account": account,#账号
                               "password": hashids_encode(passwd),#密码
                               "needUpdatePwd": needUpdatePwd,#是否强制用户首次登录时修改密码
                               "email": email,#邮箱
                               "home": home,#主目录
                               "exclude_list":exclude_list,#禁止访问路径
                               "permission": permission,#权限
                               "uploadSpeed": int(uploadSpeed * 1024 * 1024 / 8),   #上传速度限制
                               "downloadSpeed": int(downloadSpeed * 1024 * 1024 / 8),#下载速度限制
                               "syncSwitch": syncSwitch,#同步目录功能
                               "address": "",
                               "uploadSuffixLimit": uploadSuffixLimit,	# 文件格式白名单 0：不开启限制，1：开启白名单限制
                               "suffixList": suffixList,	# 文件后缀列表，传入数组
                               "emailSenderType": emailSenderType, #邮件发送方 0：以管理员配置邮箱发送  1：以用户配置邮箱发送
                               "whitelistIPSwitch" : whitelistIPSwitch ,#IP登录白名单  0：不开启限制  1：开启限制
                               "whitelistIP" : whitelistIP, #IP白名单限制列表，传入字符串
                                "company": "",
                               "accountType": 2,#1：管理员 2：普通用户 3：分享用户 4：ad域用户 5：邮箱用户  6：unix系统用户
                               "created": 0,
                            "phone": "",
                            "remark": "",
                            "status": 0,
                              "authWay": "",
                              "groupIdList":""
                        },
                          "groupIdList" : groupIdList, #关联用户组
                          "id": int(time.time()),
                          "token": token,
                          "version": "3.0.3.2"}
        respone = raysync.raysync_request(json=createuser_data)
        return respone
    except Exception as e:
        logger.exception("新建用户，错误是{}".format(e))

def selectUsers(token,query,count=10,page=1):
    #根据账号搜索用户
    if query=="":
        query = {}
    try:
        selectUsers_data = {
            "action": "SELECT_USERS",
            "count": count,
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "order": 1,
            "orderBy": "id",
            "page": page,
            "query": query,
            "token": token,
            "version": "3.0.3.2"
        }
        respone = raysync.raysync_request(json=selectUsers_data)
        return respone
    except Exception as e:
        logger.exception("根据账号搜索用户".format(e))

def deleteUsers(token,users):
    #删除用户
    try:
        deleteUsers_data = {
            "action": "DELETE_USERS",
            "clearData": False,
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "users": users, #数组形式传入
            "version": "3.0.3.2",
        }
        respone = raysync.raysync_request(json=deleteUsers_data)
        return respone
    except Exception as e:
        logger.exception("删除用户".format(e))

def admin_updateuser(token,user_id,account,passwd,name="",needUpdatePwd=1,email="",home="",addExcludeList=[],permission=4095,uploadSpeed=0,downloadSpeed=0,syncSwitch=False,
                     uploadSuffixLimit=0,suffixList=[],emailSenderType=0,whitelistIPSwitch=False,whitelistIP="",addGroupIdList=[],delGroupIdList=[]):
    #更新用户
    try:
        updateuser_data ={ "action": "UPDATE_USER",
                              "module": "WEBADMIN",
                              "device": "",
                              "user": {
                                   "name": name,#姓名
                                   "account": account,#账号
                                   "password": hashids_encode(passwd),#密码
                                   "needUpdatePwd": needUpdatePwd,#是否强制用户首次登录时修改密码
                                   "email": email,#邮箱
                                   "home": home,#主目录
                                   "addExcludeList":addExcludeList,#禁止访问路径
                                   "permission": permission,#权限
                                   "uploadSpeed": int(uploadSpeed * 1024 * 1024 / 8),   #上传速度限制
                                   "downloadSpeed": int(downloadSpeed * 1024 * 1024 / 8),#下载速度限制
                                   "syncSwitch": syncSwitch,#同步目录功能
                                   "address": "",
                                   "uploadSuffixLimit": uploadSuffixLimit,	# 文件格式白名单 0：不开启限制，1：开启白名单限制
                                   "suffixList": suffixList,	# 文件后缀列表，传入数组
                                   "emailSenderType": emailSenderType, #邮件发送方 0：以管理员配置邮箱发送  1：以用户配置邮箱发送
                                   "whitelistIPSwitch" : whitelistIPSwitch ,#IP登录白名单  0：不开启限制  1：开启限制
                                   "whitelistIP" : whitelistIP, #IP白名单限制列表，传入字符串
                                    "company": "",
                                   "accountType": 2,#1：管理员 2：普通用户 3：分享用户 4：ad域用户 5：邮箱用户  6：unix系统用户
                                   "created": int(time.time()),
                                   "id":user_id,
                                    "phone": "",
                                    "remark": "",
                                    "status": 0,
                                   "authWay": "",
                                   "groupIdList":""
                            },
                              "addGroupIdList" : addGroupIdList, #关联用户组
                              "delGroupIdList":delGroupIdList,
                              "id": int(time.time()),
                              "token": token,
                              "version": "3.0.3.2"}
        respone = raysync.raysync_request(json=updateuser_data)
        return respone
    except Exception as e:
        logger.exception("更新用户，错误是{}".format(e))

def addUserGroup(token,groupPermission,groupName,groupDownspeed=0,groupUpspeed=0):
    #添加用户组
    try:
        addUserGroup_data = {
            "action": "ADD_USERGROUP",
            "data": {
                "groupDownspeed": groupDownspeed,
                "groupHome": "",
                "groupName": groupName,
                "groupPermission": groupPermission,
                "groupUpspeed": groupUpspeed
                    },
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "version": "3.0.3.2",
        }
        respone = raysync.raysync_request(json=addUserGroup_data)
        return respone
    except Exception as e:
        logger.exception("添加用户组，错误是{}".format(e))

def delUserGroup(token,groupIds):
    #删除用户组
    try:
        delUserGroup_data = {
            "action": "DEL_USERGROUP",
            "data": {"groupIds": groupIds},
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": "gXbGm3JKVEhxV4AggsWdV2bgB1jnwL2yrGQNSvUA",
            "version": "3.0.3.2"
        }
        respone = raysync.raysync_request(json=delUserGroup_data)
        return respone
    except Exception as e:
        logger.exception("删除用户组，错误是{}".format(e))

def getUserGroup(token,selectGroupName=""):
    #搜索用户组
    try:
        getUserGroup_data = {
            "action": "GET_USERGROUP",
            "data": {"page": 1, "count": 10, "selectGroupName": selectGroupName},
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "token": token,
            "version": "3.0.3.2"
        }
        respone = raysync.raysync_request(json=getUserGroup_data)
        return respone
    except Exception as e:
        logger.exception("搜索用户组，错误是{}".format(e))

def setUserLockStatus(token,status,userId):
    #锁定和解锁用户
    try:
        setUserLockStatus_data = {
            "action": "SET_USER_LOCK_STATUS",
            "device": "",
            "id": int(time.time()),
            "module": "WEBADMIN",
            "status": status,
            "token": token,
            "userId": userId,
            "version": "3.0.3.2",
        }
        respone = raysync.raysync_request(json=setUserLockStatus_data)
        return respone
    except Exception as e:
        logger.exception("锁定和解锁用户，错误是{}".format(e))



# s=admin_upadteserver("57d7ccc66356e")
# print(s)
# h=resetFileList()
# print(h.text)
# s=setLogo()
# print(s.text)

if __name__ == "__main__":
    # title = "test1"
    # content = """测试发送内容
    # 1
    # 2
    # s
    # d
    # sfasgdasgas
    # 5325634645
    # 共发送给发货特
    # sfhioasghoia@%#$^$%@&*%^*$
    # SSDDDDDD
    # """
    # userNotice = []
    # for i in range(0,50):
    #     userNotice.append(str(i) + ":0")
    #     userNotice.append(str(i) + ":1")
    # emailLanguage = 1
    # token = "4evPOrLnw6trooZpRC3VVzey7djbg3ZVaJ7HmVwT"
    # for i in range(0,300):
    #     result = addNotice(token,title,content,userNotice,emailLanguage)
    #     print(result.text)
    # s=getAllShareLink("31dQgX0PR1U9J2m1zuewa0g1r8KlyBmZP4Z9JTzN","2020-09-20 00:00:00","2020-10-23 00:00:00",type=0)
    s=addUserGroup("gXbGm3JKVEhxV4AggsWdV2bgB1jnwL2yrGQNSvUA")
    print(s.text)