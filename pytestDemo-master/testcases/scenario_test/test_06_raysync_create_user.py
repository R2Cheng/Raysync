import pytest
import allure
from operation.admin_api import *
from operation.fe_api import *
from common.logger import logger
from common.admin_permission_ruler import decode_permission
from common.raysync_rayfile_c import rayfile_cmd
from common.encode_permission import decode_permission_1

@allure.step("获取token")
def step_1():
    respone = admin_login("admin","Test!123")
    logger.info("先获取token")
    return respone.json().get("token")

@allure.step("如创建用户存在，执行先删除改用户")
def step_2(token,account):
    result_user = selectUsers(token,{"account":account})
    user = result_user.json().get("users")
    if len(user) !=0:
        if account == user[0]["account"]:
            user_exist = True
            account_id = user[0]["id"]
        else:
            user_exist = False
            account_id = None
    else:
        user_exist = False
        account_id = None
    if user_exist:
        users = []
        users.append(account_id)
        result = deleteUsers(token,users)
        logger.info("创建用户存在，执行删除用户操作")
    else:
        logger.info("创建用户不存在，不执行删除用户操作")



@allure.step("前台退出")
def step_3(token,userId):
    result = logout(token,userId)
    result_data = result.json().get("result")
    logger.info("{}:前台退出,退出结果为：{}".format(userId,result_data))

@allure.step("账户文件及文件夹初始化")
def step_4(host,account,password):
    output_upload,error_code_upload = rayfile_cmd(address=host, user=account, password=password, operation="upload",destination="/", source="E:\\testFile\\1M.txt")
    output_upload2, error_code_upload2 = rayfile_cmd(address=host, user=account, password=password, operation="upload", destination="/",source="E:\\testFile\\2M.txt")
    out_mkdir, error_code_mkdir = rayfile_cmd(address=host, user=account, password=password, operation="mkdir",destination="/test1", source="")
    out_mkdir2, error_code_mkdir2 = rayfile_cmd(address=host, user=account, password=password, operation="mkdir",destination="/test2", source="")
    logger.info("账户文件及文件夹初始化结果为：{}{}{}{}".format(error_code_upload, error_code_upload2,error_code_mkdir,error_code_mkdir2))

@allure.step("删除用户组")
def step_5(token,groupName):
    get_result = getUserGroup(token,groupName)
    data = get_result.json().get("data")
    if len(data["groupList"]) !=0:
        groupId = data["groupList"][0]["groupId"]
        groupIds = []
        groupIds.append(groupId)
        del_result = delUserGroup(token,groupIds)
        logger.info("删除用户组{}成功".format(del_result))
    else:
        logger.info("用户组不存在，不用进行删除")


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：创建新用户")
class TestCreateUser():

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("默认参数新用户创建-创建结果验证--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_01(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token,account)
        logger.info("*************** 开始执行用例 ***************")

        logger.info("*************** 创建用户结果 ***************")
        result_createUser = admin_createuser(token,name=name,account=account,passwd=password,needUpdatePwd=needUpdatapwd,email=email,permission=permission,emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")
        logger.info("创建用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_createUser.json().get("result")))
        logger.info("创建用户信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_createUser.json().get("message")))
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("默认参数新用户创建-使用账号首次登录修改密码验证--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_02(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")
        logger.info("*************** 使用account首次登录验证 ***************")
        result_needUpdatePwd = feLogin(account,password)
        assert result_needUpdatePwd.json().get("result") == 1076
        assert "need update default password" in result_needUpdatePwd.json().get("message")
        logger.info("使用account首次登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(1076, result_needUpdatePwd.json().get("result")))
        logger.info("使用account首次登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_needUpdatePwd.json().get("message")))

        logger.info("*************** 首次登录修改密码验证 ***************")
        result_initpass = updateUserInitPass(account,password,password)
        assert result_initpass.json().get("result") == 0
        assert "OK" in result_initpass.json().get("message")
        logger.info("首次登录修改密码验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_initpass.json().get("result")))
        logger.info("使用account首次登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_initpass.json().get("message")))

        logger.info("*************** 使用首次登录修改密码登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用首次登录修改密码登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用首次登录修改密码登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("默认参数新用户创建-使用邮箱首次登录修改密码验证--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_03(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")
        logger.info("*************** 使用account首次登录验证 ***************")
        result_needUpdatePwd = feLogin(account, password)
        assert result_needUpdatePwd.json().get("result") == 1076
        assert "need update default password" in result_needUpdatePwd.json().get("message")
        logger.info("使用account首次登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(1076, result_needUpdatePwd.json().get("result")))
        logger.info("使用account首次登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_needUpdatePwd.json().get("message")))

        logger.info("*************** 首次登录修改密码验证 ***************")
        result_initpass = updateUserInitPass(account, password, password)
        assert result_initpass.json().get("result") == 0
        assert "OK" in result_initpass.json().get("message")
        logger.info("首次登录修改密码验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_initpass.json().get("result")))
        logger.info("使用account首次登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_initpass.json().get("message")))

        logger.info("*************** 使用首次登录修改密码登录验证 ***************")
        result_feLogin = feLogin(account, password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用首次登录修改密码登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用首次登录修改密码登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("默认参数新用户创建-使用账号登录前台后，进行姓名、账号、邮箱、权限、邮件发送方验证--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_04(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")
        logger.info("*************** 使用邮箱首次登录验证 ***************")
        result_getAccount = getAccount(email)
        assert result_getAccount.json().get("result") == 0
        assert "OK" in result_getAccount.json().get("message")
        assert result_getAccount.json().get("account") == account
        logger.info("使用邮箱首次登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_getAccount.json().get("result")))
        logger.info("使用邮箱首次登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_getAccount.json().get("message")))
        logger.info("使用邮箱首次登录验证信息获取account ==>> 期望结果：{}， 实际结果：【 {} 】".format(account, result_getAccount.json().get("account")))

        logger.info("*************** 邮箱首次登录修改密码验证 ***************")
        result_initpass = updateUserInitPass(result_getAccount.json().get("account"),password,password)
        assert result_initpass.json().get("result") == 0
        assert "OK" in result_initpass.json().get("message")
        logger.info("邮箱首次登录修改密码验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_initpass.json().get("result")))
        logger.info("邮箱首次登录修改密码验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_initpass.json().get("message")))

        logger.info("*************** 邮箱首次登录修改密码登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("邮箱首次登录修改密码登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("邮箱首次登录修改密码登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 进行姓名、账号、邮箱、权限、邮件发送方验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_selectUser = selectUser(fe_token, fe_account, fe_userId)
        user_account = result_selectUser.json().get("user")["account"]
        user_name = result_selectUser.json().get("user")["name"]
        user_email = result_selectUser.json().get("user")["email"]
        user_permission = result_selectUser.json().get("user")["permission"]
        user_emailSenderType = result_selectUser.json().get("user")["emailSenderType"]
        assert user_account == account
        assert user_name == name
        assert user_email == email
        assert user_permission == permission
        assert user_emailSenderType == emailSenderType
        logger.info("姓名验证name ==>> 期望结果：{}， 实际结果：【 {} 】".format(name, user_name))
        logger.info("账号验证account ==>> 期望结果：{}， 实际结果：【 {} 】".format(account, user_account))
        logger.info("邮箱验证email ==>> 期望结果：{}， 实际结果：【 {} 】".format(email, user_email))
        logger.info("前台权限验证permission ==>> 期望结果：{}， 实际结果：【 {} 】".format(permission, user_permission))
        logger.info("邮件发送方验证emailSenderType ==>> 期望结果：{}， 实际结果：【 {} 】".format(emailSenderType, user_emailSenderType))

        logger.info("*************** 同步目录验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_userId = result_feLogin.json().get("userId")
        result_sync = getComplexSyncSwitchNoVersion(fe_token, fe_userId)
        sync_result = result_sync.json().get("data")["syncSwitch"]
        assert sync_result == False

        logger.info("同步目录验证groupName ==>> 期望结果：{}， 实际结果：【 {} 】".format(False, sync_result))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("默认参数新用户创建-权限rayfile-c验证--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_05(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        host = testcase_data["host"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 使用account登录验证 ***************")
        result_account = feLogin(account, password)
        assert result_account.json().get("result") == 0
        assert "OK" in result_account.json().get("message")
        logger.info("使用account登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_account.json().get("result")))
        logger.info("使用account登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_account.json().get("message")))

        logger.info("*************** rayfile-c权限验证 ***************")
        permission_data = decode_permission(permission)
        out_upload, error_code_upload = rayfile_cmd(address=host, user=account, password=password, operation="upload",destination="/", source="E:\\testFile\\4M.txt")
        out_list, error_code_list = rayfile_cmd(address=host, user=account, password=password,operation="list", destination="/", source="")
        out_download, error_code_download = rayfile_cmd(address=host, user=account, password=password,operation="download", destination="E:\\testFile\\download",source="/4M.txt")  # download
        out_mkdir, error_code_mkdir = rayfile_cmd(address=host, user=account, password=password,operation="mkdir", destination="/cmdmkdir", source="")  # mkdir
        out_rename, error_code_rename = rayfile_cmd(address=host, user=account, password=password,operation="rename", destination="test1", source="/cmdmkdir")  # rename
        out_copy, error_code_copy = rayfile_cmd(address=host, user=account, password=password,operation="copy", destination="/test1/test.txt",source="/4M.txt")  # copy
        out_move, error_code_move = rayfile_cmd(address=host, user=account, password=password,operation="move", destination="/test1/ssss.txt",source="/4M.txt")  # move
        out_remove, error_code_remove = rayfile_cmd(address=host, user=account, password=password, operation="remove",destination="/test1", source="")  # remove
        if permission_data["list"]:
            code_list = None
        else:
            code_list = 16
        if permission_data["upload"]:
            code_upload = None
        else:
            code_upload = 16
        if permission_data["download"]:
            code_download = None
        else:
            code_download = 16
        if permission_data["mkdir"]:
            code_mkdir = None
        else:
            code_mkdir = 16
        if permission_data["rename"]:
            code_rename = None
        else:
            code_rename = 16
        if permission_data["copy"]:
            code_copy = "0"
        else:
            code_copy = 16
        if permission_data["move"]:
            code_move = "0"
        else:
            code_move = 16
        if permission_data["remove"]:
            code_remove = None
        else:
            code_remove = 16
        assert error_code_list == code_list
        assert error_code_upload == code_upload
        assert error_code_download == code_download
        assert error_code_mkdir == code_mkdir
        assert error_code_rename == code_rename
        assert error_code_remove == code_remove
        assert error_code_copy == code_copy
        assert error_code_move == code_move
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_list, error_code_list))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_upload, error_code_upload))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_download, error_code_download))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_mkdir, error_code_mkdir))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_rename, error_code_rename))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_remove, error_code_remove))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, error_code_copy))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_move, error_code_move))
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("全部禁止权限校验-权限rayfile-c验证--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_06(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        host = testcase_data["host"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        logger.info("*************** 建立全部权限的用户 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=4095,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 先创建用户文件夹及上传文件，避免因无文件导致判断失败 ***************")
        step_4(host,account,password)
        logger.info("*************** 使用account登录验证 ***************")
        result_account = feLogin(account, password)
        assert result_account.json().get("result") == 0
        assert "OK" in result_account.json().get("message")
        logger.info("使用account登录验证结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_account.json().get("result")))
        logger.info("使用account登录验证信息message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_account.json().get("message")))

        logger.info("*************** 修改用户权限为全部禁止 ***************")
        result_updataUser = admin_updateuser(token,name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,user_id=result_createUser.json().get("userId"))
        assert result_updataUser.json().get("result") == 0
        assert "OK" in result_updataUser.json().get("message")
        logger.info("修改用户权限为全部禁止result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_updataUser.json().get("result")))
        logger.info( "修改用户权限为全部禁止message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_updataUser.json().get("message")))
        feLogin(account,password)
        time.sleep(10)
        logger.info("*************** rayfile-c权限验证 ***************")
        permission_data = decode_permission(permission)
        if permission_data["list"]:
            code_list = None
        else:
            code_list = 16
        if permission_data["upload"]:
            code_upload = None
        else:
            code_upload = 16
        if permission_data["download"]:
            code_download = None
        else:
            code_download = 16
        if permission_data["mkdir"]:
            code_mkdir = None
        else:
            code_mkdir = 16
        if permission_data["rename"]:
            code_rename = None
        else:
            code_rename = 16
        if permission_data["copy"]:
            code_copy = "0"
        else:
            code_copy = 16
        if permission_data["move"]:
            code_move = "0"
        else:
            code_move = 16
        if permission_data["remove"]:
            code_remove = None
        else:
            code_remove = 16

        out_upload, error_code_upload = rayfile_cmd(address=host, user=account, password=password, operation="upload",destination="/", source="E:\\testFile\\44M.txt")
        assert error_code_upload == code_upload
        out_download, error_code_download = rayfile_cmd(address=host, user=account, password=password,operation="download", destination="E:\\testFile\\download",source="/1M.txt")  # download
        assert error_code_download == code_download
        out_mkdir, error_code_mkdir = rayfile_cmd(address=host, user=account, password=password,operation="mkdir", destination="/cmdmkdir", source="")  # mkdir
        assert error_code_mkdir == code_mkdir
        out_rename, error_code_rename = rayfile_cmd(address=host, user=account, password=password,operation="rename", destination="test5", source="/test2")  # rename
        assert error_code_rename == code_rename
        out_copy, error_code_copy = rayfile_cmd(address=host, user=account, password=password,operation="copy", destination="/test1/test.txt",source="/2M.txt")  # copy
        assert error_code_copy == code_copy
        out_move, error_code_move = rayfile_cmd(address=host, user=account, password=password,operation="move", destination="/test1/ssss.txt",source="/2M.txt")  # move
        assert error_code_move == code_move
        out_remove, error_code_remove = rayfile_cmd(address=host, user=account, password=password, operation="remove",destination="/test1", source="")  # remove
        assert error_code_remove == code_remove
        out_list, error_code_list = rayfile_cmd(address=host, user=account, password=password, operation="list",destination="/", source="")
        assert error_code_list == code_list
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_list, error_code_list))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_upload, error_code_upload))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_download, error_code_download))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_mkdir, error_code_mkdir))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_rename, error_code_rename))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_remove, error_code_remove))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, error_code_copy))
        logger.info("list结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(code_move, error_code_move))
        logger.info("*************** 结束执行用例 ***************")



    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("默认参数新用户创建-各种权限组合使用前台接口验证--预期成功")
    @pytest.mark.multiple
    #@pytest.mark.skip(reason="校验时间过长，调试阶段先暂停")
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_07(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")
        permission_list = decode_permission_1()
        for permission in permission_list:
            logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
            step_2(token, account)

            result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
            assert result_createUser.json().get("result") == except_result
            assert except_msg in result_createUser.json().get("message")

            logger.info("*************** 使用account登录验证 ***************")
            result_feLogin = feLogin(account,password)
            assert result_feLogin.json().get("result") == 0
            assert "OK" in result_feLogin.json().get("message")
            logger.info("使用account登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
            logger.info("使用account登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

            logger.info("*************** 进行权限验证 ***************")
            fe_token = result_feLogin.json().get("token")
            fe_account = result_feLogin.json().get("account")
            fe_userId = result_feLogin.json().get("userId")
            result_selectUser = selectUser(fe_token, fe_account, fe_userId)
            user_permission = result_selectUser.json().get("user")["permission"]
            assert user_permission == permission
            logger.info("前台权限验证permission ==>> 期望结果：{}， 实际结果：【 {} 】".format(permission, user_permission))

            logger.info("*************** 退出登录前台 ***************")
            step_3(fe_token,fe_userId)
            #time.sleep(1)
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-全部权限（4095）用户组校验--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_08(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        groupName = testcase_data["groupName"]
        groupPermission = testcase_data["groupPermission"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除该用户 ***************")
        step_2(token, account)
        logger.info("*************** 如创建用户组存在，执行先删除该用户组 ***************")
        step_5(token,groupName)
        logger.info("*************** 开始执行用例 ***************")

        logger.info("*************** 创建用户组 ***************")
        addUserGroup(token,groupPermission,groupName)
        groupId = getUserGroup(token,groupName).json().get("data")["groupList"][0]["groupId"]
        groupIds =[]
        groupIds.append(groupId)
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,groupIdList=groupIds)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 使用account登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用account登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用account登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 用户组校验验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_selectUser = selectUser(fe_token, fe_account, fe_userId)
        groupList = result_selectUser.json().get("user")["groupList"]
        for group in groupList:
            groupName_r = group["groupName"]
            groupId_r = group["groupId"]
            groupPermission_r = group["groupPermission"]
            assert groupName_r == groupName
            assert groupId_r == groupId
            assert groupPermission_r == groupPermission
            logger.info("用户组名验证groupName ==>> 期望结果：{}， 实际结果：【 {} 】".format(groupName_r, groupName))
            logger.info("用户组Id校验groupId ==>> 期望结果：{}， 实际结果：【 {} 】".format(groupId_r, groupId))
            logger.info("用户组权限校验groupPermission ==>> 期望结果：{}， 实际结果：【 {} 】".format(groupPermission_r, groupPermission))
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-没有权限（0）用户组校验--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_user_09(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        groupName = testcase_data["groupName"]
        groupPermission = testcase_data["groupPermission"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除该用户 ***************")
        step_2(token, account)
        logger.info("*************** 如创建用户组存在，执行先删除该用户组 ***************")
        step_5(token,groupName)
        logger.info("*************** 开始执行用例 ***************")

        logger.info("*************** 创建用户组 ***************")
        addUserGroup(token,groupPermission,groupName)
        groupId = getUserGroup(token,groupName).json().get("data")["groupList"][0]["groupId"]
        groupIds =[]
        groupIds.append(groupId)
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,groupIdList=groupIds)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 使用account登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用account登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用account登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 用户组校验验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_selectUser = selectUser(fe_token, fe_account, fe_userId)
        groupList = result_selectUser.json().get("user")["groupList"]
        for group in groupList:
            groupName_r = group["groupName"]
            groupId_r = group["groupId"]
            groupPermission_r = group["groupPermission"]
            assert groupName_r == groupName
            assert groupId_r == groupId
            assert groupPermission_r == groupPermission
            logger.info("用户组名验证groupName ==>> 期望结果：{}， 实际结果：【 {} 】".format(groupName_r, groupName))
            logger.info("用户组Id校验groupId ==>> 期望结果：{}， 实际结果：【 {} 】".format(groupId_r, groupId))
            logger.info("用户组权限校验groupPermission ==>> 期望结果：{}， 实际结果：【 {} 】".format(groupPermission_r, groupPermission))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-有同步目录功能校验--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_syncSwitch_10(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        syncSwitch = testcase_data["syncSwitch"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除该用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,syncSwitch=syncSwitch)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 使用account登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用account登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用account登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 同步目录验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_userId = result_feLogin.json().get("userId")
        result_sync = getComplexSyncSwitchNoVersion(fe_token,fe_userId)
        sync_result = result_sync.json().get("data")["syncSwitch"]
        assert sync_result == syncSwitch

        logger.info("同步目录验证syncSwitch ==>> 期望结果：{}， 实际结果：【 {} 】".format(syncSwitch, sync_result))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-有文件格式白名单限制（没有输入文件后缀列表）--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_uploadSuffixLimit_11(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        uploadSuffixLimit = testcase_data["uploadSuffixLimit"]
        suffixList = testcase_data["suffixList"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除该用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,uploadSuffixLimit=uploadSuffixLimit,suffixList=suffixList)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 使用account登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用account登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用account登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 文件格式白名单验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_selectUser = selectUser(fe_token, fe_account, fe_userId)
        uploadSuffixLimit_result = result_selectUser.json().get("user")["uploadSuffixLimit"]
        suffixList_len = len(result_selectUser.json().get("user")["suffixList"])
        assert uploadSuffixLimit_result == uploadSuffixLimit
        assert suffixList_len == 0
        logger.info("文件格式白名单验证uploadSuffixLimit ==>> 期望结果：{}， 实际结果：【 {} 】".format(uploadSuffixLimit, uploadSuffixLimit_result))
        logger.info("文件格式白名单验证suffixList_len ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, suffixList_len))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-有文件格式白名单限制（输入exe，txt）--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_uploadSuffixLimit_12(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        uploadSuffixLimit = testcase_data["uploadSuffixLimit"]
        suffixList = testcase_data["suffixList"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除该用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,uploadSuffixLimit=uploadSuffixLimit,suffixList=suffixList)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")

        logger.info("*************** 使用account登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("使用account登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("使用account登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 文件格式白名单验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_selectUser = selectUser(fe_token, fe_account, fe_userId)
        uploadSuffixLimit_result = result_selectUser.json().get("user")["uploadSuffixLimit"]
        suffixList_result = result_selectUser.json().get("user")["suffixList"]
        assert uploadSuffixLimit_result == uploadSuffixLimit
        for i in suffixList_result:
            assert i in suffixList
        logger.info("文件格式白名单验证uploadSuffixLimit ==>> 期望结果：{}， 实际结果：【 {} 】".format(uploadSuffixLimit, uploadSuffixLimit_result))
        logger.info("文件格式白名单验证suffixList ==>> 期望结果：{}， 实际结果：【 {} 】".format(suffixList, suffixList_result))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-以用户配置邮箱发送--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_emailSenderType_13(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")
        logger.info("*************** 邮箱登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("邮箱首次登录修改密码登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("邮箱首次登录修改密码登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 用户配置邮箱验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_emailSenderType = selectUser(fe_token,fe_account,fe_userId)
        emailSenderType_result = result_emailSenderType.json().get("user")["emailSenderType"]
        assert emailSenderType_result == emailSenderType
        logger.info("同步目录验证groupName ==>> 期望结果：{}， 实际结果：【 {} 】".format(emailSenderType, emailSenderType_result))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-设置登录IP白名单（只开启，不设置白名单）--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_whitelistIPSwitch_14(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        whitelistIPSwitch = testcase_data["whitelistIPSwitch"]
        whitelistIP = testcase_data["whitelistIP"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,whitelistIPSwitch=whitelistIPSwitch,whitelistIP=whitelistIP)
        assert result_createUser.json().get("result") == except_result
        assert except_msg in result_createUser.json().get("message")
        logger.info("*************** 邮箱登录验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == 0
        assert "OK" in result_feLogin.json().get("message")
        logger.info("邮箱首次登录修改密码登录验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_feLogin.json().get("result")))
        logger.info("邮箱首次登录修改密码登录验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result_feLogin.json().get("message")))

        logger.info("*************** 设置登录IP白名单验证 ***************")
        fe_token = result_feLogin.json().get("token")
        fe_account = result_feLogin.json().get("account")
        fe_userId = result_feLogin.json().get("userId")
        result_white = selectUser(fe_token,fe_account,fe_userId)
        white_result = result_white.json().get("user")["whitelistIPSwitch"]
        whitelistIP_result = result_white.json().get("user")["whitelistIP"]
        assert white_result == whitelistIPSwitch
        assert whitelistIP_result == whitelistIP
        logger.info("设置登录IP whitelistIPSwitch ==>> 期望结果：{}， 实际结果：【 {} 】".format(whitelistIPSwitch, white_result))
        logger.info("设置登录IP，ip白名单列表 whitelistIP ==>> 期望结果：{}， 实际结果：【 {} 】".format(whitelistIP, whitelistIP_result))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-设置登录IP白名单，设置多个ip地址，在非设置ip下登录失败--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_whitelistIPSwitch_15(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        whitelistIPSwitch = testcase_data["whitelistIPSwitch"]
        whitelistIP = testcase_data["whitelistIP"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,whitelistIPSwitch=whitelistIPSwitch,whitelistIP=whitelistIP)
        assert result_createUser.json().get("result") == 0
        assert "OK" in result_createUser.json().get("message")

        logger.info("*************** 账号登录IP白名单验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == except_result
        assert except_msg in result_feLogin.json().get("message")
        logger.info("账号登录IP白名单验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_feLogin.json().get("result")))
        logger.info("账号登录IP白名单验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_feLogin.json().get("message")))

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-设置登录IP白名单，设置多个ip地址，在设置ip下登录成功--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_whitelistIPSwitch_16(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        whitelistIPSwitch = testcase_data["whitelistIPSwitch"]
        whitelistIP = testcase_data["whitelistIP"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,whitelistIPSwitch=whitelistIPSwitch,whitelistIP=whitelistIP)
        assert result_createUser.json().get("result") == 0
        assert "OK" in result_createUser.json().get("message")

        logger.info("*************** 账号登录IP白名单验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == except_result
        assert except_msg in result_feLogin.json().get("message")
        logger.info("账号登录IP白名单验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_feLogin.json().get("result")))
        logger.info("账号登录IP白名单验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_feLogin.json().get("message")))

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-设置登录IP白名单，设置多个ip地址，在设置ip下登录成功--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_whitelistIPSwitch_17(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        whitelistIPSwitch = testcase_data["whitelistIPSwitch"]
        whitelistIP = testcase_data["whitelistIP"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,whitelistIPSwitch=whitelistIPSwitch,whitelistIP=whitelistIP)
        assert result_createUser.json().get("result") == 0
        assert "OK" in result_createUser.json().get("message")

        logger.info("*************** 账号登录IP白名单验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == except_result
        assert except_msg in result_feLogin.json().get("message")
        logger.info("账号登录IP白名单验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_feLogin.json().get("result")))
        logger.info("账号登录IP白名单验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_feLogin.json().get("message")))

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-设置登录IP白名单，设置多个ip地址，在设置ip下登录成功--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_whitelistIPSwitch_18(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        whitelistIPSwitch = testcase_data["whitelistIPSwitch"]
        whitelistIP = testcase_data["whitelistIP"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType,whitelistIPSwitch=whitelistIPSwitch,whitelistIP=whitelistIP)
        assert result_createUser.json().get("result") == 0
        assert "OK" in result_createUser.json().get("message")

        logger.info("*************** 账号登录IP白名单验证 ***************")
        result_feLogin = feLogin(account,password)
        assert result_feLogin.json().get("result") == except_result
        assert except_msg in result_feLogin.json().get("message")
        logger.info("账号登录IP白名单验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_feLogin.json().get("result")))
        logger.info("账号登录IP白名单验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_feLogin.json().get("message")))

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-创建已存在的邮箱的账号，创建失败--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_email_only_19(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == 0
        assert "OK" in result_createUser.json().get("message")

        logger.info("*************** 创建已存在的邮箱的账号验证 ***************")
        result_createUser2 = admin_createuser(token, name=name, account="test2", passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser2.json().get("result") == except_result
        assert except_msg in result_createUser2.json().get("message")
        logger.info("创建已存在的邮箱的账号验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_createUser2.json().get("result")))
        logger.info("创建已存在的邮箱的账号验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_createUser2.json().get("message")))

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("新用户创建-创建已存在的账号，创建失败--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_create_account_only_20(self, testcase_data):
        name = testcase_data["name"]
        account = testcase_data["account"]
        password = testcase_data["password"]
        needUpdatapwd = testcase_data["needUpdatapwd"]
        email = testcase_data["email"]
        permission = testcase_data["permission"]
        emailSenderType = testcase_data["emailSenderType"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 如创建用户存在，执行先删除改用户 ***************")
        step_2(token, account)
        logger.info("*************** 开始执行用例 ***************")
        result_createUser = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email=email, permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser.json().get("result") == 0
        assert "OK" in result_createUser.json().get("message")

        logger.info("*************** 创建已存在的账号验证 ***************")
        result_createUser2 = admin_createuser(token, name=name, account=account, passwd=password,
                                             needUpdatePwd=needUpdatapwd, email="test1@email.coim", permission=permission,
                                             emailSenderType=emailSenderType)
        assert result_createUser2.json().get("result") == except_result
        assert except_msg in result_createUser2.json().get("message")
        logger.info("创建已存在的邮箱的账号验证result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_createUser2.json().get("result")))
        logger.info("创建已存在的邮箱的账号验证message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_createUser2.json().get("message")))


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_06_raysync_create_user.py"])