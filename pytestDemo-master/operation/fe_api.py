import time,datetime,string,random
from api.user import raysync_fe,api_fe_url
from common.logger import logger
from common.encry_hash import hashids_encode

def feLogin(accout,password):
    #登录前台
    try:
        accout = hashids_encode(accout)
        password = hashids_encode(password)
        feLogin_data = {
            "UK": accout + password,
            "action":"login",
            "device":"",
            "id":int(time.time()),
            "module":"WEBUI",
            "version":"3.0.3.2"
        }
        response = raysync_fe.raysync_fe_login_request(json=feLogin_data)
        return response
    except Exception as e:
        logger.exception("登录前台，错误是{}".format(e))

def createUrl(token,userId,expireTime=0,shareEmail="",notifyEmail="",shareEmailContent="",emailLanguage=0,shareFiles=[""],shareUrlType=0):
    #邀请上传
    try:
        if expireTime != 0:
            expire_time = datetime.datetime.now() + datetime.timedelta(days=expireTime)
            expire_time_f = expire_time.strftime("%Y-%m-%d %H:%M:%S")
            expireTime = int(time.mktime(time.strptime(expire_time_f,"%Y-%m-%d %H:%M:%S")))
        else:
            pass
        password = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        createUrl_data = {
            "account": "test1",
            "accountType": 2,
            "action": "CREATEURL",
            "device": "",
            "emailLanguage": emailLanguage,
            "id": int(time.time()),
            "module": "WEBUI",
            "notifyEmail": notifyEmail,
            "shareAllowDownload": 1,
            "shareBaseUrl": api_fe_url + "/share/",
            "shareEmail": shareEmail,
            "shareEmailContent": shareEmailContent,
            "shareExpireTime": expireTime, #失效时间
            "shareFiles": shareFiles,
            "shareServerPath": "/",
            "shareSrcType": 2,
            "shareUrlPasswd": password,
            "shareUrlType": shareUrlType, #0为邀请上传 1为分享下载
            "token": token,
            "userId": userId,
            "version": "3.0.3.2",
        }
        response = raysync_fe.raysync_fe_request(json=createUrl_data)
        return response
    except Exception as e:
        logger.exception("更新服务器信息，错误是{}".format(e))

def checkUrl(url):
    #测试邀请上传和下载链接
    try:
        checkUrl_data = {
            "action":"CHECKURL",
            "device":"",
            "id":int(time.time()),
            "module":"WEBUI",
            "url":url,
            "version":"3.0.3.2"
        }
        response = raysync_fe.raysync_fe_request(json=checkUrl_data)
        return response
    except Exception as e:
        logger.exception("测试邀请上传和下载链接，错误是{}".format(e))

def checkPasswd(url,passwd):
    #测试邀请上传和下载链接密码
    try:
        checkPasswd_data = {
            "action":"CHECKPASSWD",
            "device":"",
            "id":int(time.time()),
            "module":"WEBUI",
            "passwd": passwd,
            "url": url,
            "version": "3.0.3.2"
        }
        response = raysync_fe.raysync_fe_request(json=checkPasswd_data)
        return response
    except Exception as e:
        logger.exception("测试邀请上传和下载链接密码，错误是{}".format(e))

def updateUserInitPass(account,oldPassword,newPassword):
    #首次登录修改密码
    try:
        updateUserInitPass_data = {
            "account": hashids_encode(account),
            "action": "UPDATE_USER_INITPASS",
            "device": "",
            "id": int(time.time()),
            "module": "WEBUI",
            "newPassword": hashids_encode(newPassword),
            "oldPassword": hashids_encode(oldPassword),
            "password": oldPassword,
            "version": "3.0.3.2"
        }
        response = raysync_fe.raysync_fe_request(json=updateUserInitPass_data)
        return response
    except Exception as e:
        logger.exception("测试邀请上传和下载链接密码，错误是{}".format(e))

def getAccount(email):
    #使用邮箱登录，通过邮箱获取账号
    try:
        getAccount_data = {
            "action": "get_account",
            "device": "",
            "email": email,
            "id": int(time.time()),
            "module": "WEBUI",
            "version": "3.0.3.2"
        }
        response = raysync_fe.raysync_fe_login_request(json=getAccount_data)
        return response
    except Exception as e:
        logger.exception("使用邮箱登录，通过邮箱获取账号，错误是{}".format(e))

def selectUser(token,account,userId):
    #获取前台登录后用户信息
    try:
        selectUser_data = {
            "account": hashids_encode(account),
            "action": "SELECT_USER",
            "device": "",
            "id": int(time.time()),
            "module": "WEBUI",
            "token": token,
            "userId": userId,
            "version": "3.0.3.2",
        }
        response = raysync_fe.raysync_fe_request(json=selectUser_data)
        return response
    except Exception as e:
        logger.exception("获取前台登录后用户信息，错误是{}".format(e))

def logout(token,userId):
    #退出前台
    try:
        logout_data = {
            "action":"logout",
            "device":"",
            "id":int(time.time()),
            "module":"WEBUI",
            "token":token,
            "userId": userId,
            "version": "3.0.3.2"
        }
        response = raysync_fe.raysync_fe_request(json=logout_data)
        return response
    except Exception as e:
        logger.exception("退出前台，错误是{}".format(e))

def getComplexSyncSwitchNoVersion(token,userId):
    #查看镭速用户是否有同步目录的权限
    try:
        getComplexSyncSwitchNoVersion_data = {
            "action": "GET_COMPLEX_SYNC_SWITCH_NO_VERSION",
            "data": {"userId":userId},
            "module": "WEBUI",
            "token": token,
            "version": "3.0.3.2"
        }
        response = raysync_fe.raysync_fe_request(json=getComplexSyncSwitchNoVersion_data)
        return response
    except Exception as e:
        logger.exception("查看镭速用户是否有同步目录的权限，错误是{}".format(e))

s = createUrl("y9kNVqlewRipYW2RwsbyYQw6jvKbY7BEvK4f9vJq","1",expireTime=1,shareUrlType=1,shareFiles=["1","2","22220M.txt"])
print(s.text)