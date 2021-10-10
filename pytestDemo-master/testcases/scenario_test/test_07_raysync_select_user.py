import pytest
import allure,random
from operation.admin_api import *
from operation.fe_api import *
from common.logger import logger
from common.login_selenium import thread_login
from time import sleep


@allure.step("获取token")
def step_1():
    respone = admin_login("admin","Test!123")
    logger.info("先获取token")
    return respone.json().get("token")

@allure.step("使用浏览器登录5个用户")
def step_2():
    thread_login()
    sleep(15)

def step_3(token):
    logger.info("现有账号锁定情况，有锁定的先解锁")
    unlockId = []
    allUserId = []
    result_1 = selectUsers(token,"")
    num = int(result_1.json().get("totalCount")/10)
    for i in result_1.json().get("users"):
        allUserId.append(i["id"])
        if i["userLockedFlag"]:
            unlockId.append(i["id"])
    if num >=1 and result_1.json().get("totalCount") !=10:
        for i in range(num+1):
            result = selectUsers(token,"",page=i+1)
            for i in result.json().get("users"):
                allUserId.append(i["id"])
                if i["userLockedFlag"]:
                    unlockId.append(i["id"])
    for i in unlockId:
        setUserLockStatus(token,False,i)
    logger.info("获取5个账号id，进行锁定操作")
    lockId = random.sample(allUserId,5)
    for i in lockId:
        setUserLockStatus(token,True,i)

@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：搜索用户")
class TestSelectUser():

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("搜索用户姓名-中文搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_01(self, testcase_data):
        query1 = testcase_data["query1"]
        query2 = testcase_data["query2"]
        query3 = testcase_data["query3"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")
        logger.info("*************** 搜索中文名相同多个用户结果检验 ***************")
        userResult_1 = selectUsers(token,{"name":query1["name"]})
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))
        userNum1 = userResult_1.json().get("totalCount")
        userNameList = []
        for i in userResult_1.json().get("users"):
            userNameList.append(i["name"])
        for i in userNameList:
            assert query1["name"] in i
        assert userNum1 == query1["totalCount"]
        logger.info("搜索中文名相同多个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))

        logger.info("*************** 搜索中文名一个用户结果检验 ***************")
        userResult_2 = selectUsers(token, {"name": query2["name"]})
        assert userResult_2.json().get("result") == except_result
        assert except_msg in userResult_2.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_2.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_2.json().get("message")))
        userNum2 = userResult_2.json().get("totalCount")
        username = userResult_2.json().get("users")[0]["name"]
        assert userNum2 == query2["totalCount"]
        assert username == query2["name"]
        logger.info("搜索中文名一个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["totalCount"], userNum2))
        logger.info("搜索中文名一个用户结果username ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["name"], username))

        logger.info("*************** 搜索中文名无结果检验 ***************")
        userResult_3 = selectUsers(token, {"name": query3["name"]})
        assert userResult_3.json().get("result") == except_result
        assert except_msg in userResult_3.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_3.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_3.json().get("message")))
        userNum3 = userResult_3.json().get("totalCount")
        assert userNum3 == query3["totalCount"]
        logger.info("搜索中文名相同多个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query3["totalCount"], userNum3))

        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("搜索用户姓名-英文搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_02(self, testcase_data):
        query1 = testcase_data["query1"]
        query2 = testcase_data["query2"]
        query3 = testcase_data["query3"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")
        logger.info("*************** 搜索中文名相同多个用户结果检验 ***************")
        userResult_1 = selectUsers(token, {"name": query1["name"]})
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))
        userNum1 = userResult_1.json().get("totalCount")
        userNameList = []
        for i in userResult_1.json().get("users"):
            userNameList.append(i["name"])
        for i in userNameList:
            assert query1["name"] in i
        assert userNum1 == query1["totalCount"]
        logger.info("搜索中文名相同多个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))

        logger.info("*************** 搜索中文名一个用户结果检验 ***************")
        userResult_2 = selectUsers(token, {"name": query2["name"]})
        assert userResult_2.json().get("result") == except_result
        assert except_msg in userResult_2.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_2.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_2.json().get("message")))
        userNum2 = userResult_2.json().get("totalCount")
        username = userResult_2.json().get("users")[0]["name"]
        assert userNum2 == query2["totalCount"]
        assert username == query2["name"]
        logger.info("搜索中文名一个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["totalCount"], userNum2))
        logger.info("搜索中文名一个用户结果username ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["name"], username))

        logger.info("*************** 搜索中文名无结果检验 ***************")
        userResult_3 = selectUsers(token, {"name": query3["name"]})
        assert userResult_3.json().get("result") == except_result
        assert except_msg in userResult_3.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_3.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_3.json().get("message")))
        userNum3 = userResult_3.json().get("totalCount")
        assert userNum3 == query3["totalCount"]
        logger.info("搜索中文名相同多个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query3["totalCount"], userNum3))

        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("搜索用户账号-账号搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_03(self, testcase_data):
        query1 = testcase_data["query1"]
        query2 = testcase_data["query2"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")
        logger.info("*************** 搜索账号-一个用户结果检验 ***************")
        userResult_1 = selectUsers(token,{"account":query1["account"]})
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))
        userNum1 = userResult_1.json().get("totalCount")
        userAccount = userResult_1.json().get("users")[0]["account"]
        assert userNum1 == query1["totalCount"]
        assert userAccount == query1["account"]
        logger.info("搜索账号-一个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))
        logger.info("搜索账号-一个用户结果userAccount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["account"], userAccount))

        logger.info("*************** 搜索账号-无结果检验 ***************")
        userResult_2 = selectUsers(token, {"account": query2["account"]})
        assert userResult_2.json().get("result") == except_result
        assert except_msg in userResult_2.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_2.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_2.json().get("message")))
        userNum2 = userResult_2.json().get("totalCount")
        assert userNum2 == query2["totalCount"]
        logger.info("搜索账号-无结果结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["totalCount"], userNum2))

        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("搜索用户账号-账号搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_04(self, testcase_data):
        query1 = testcase_data["query1"]
        query2 = testcase_data["query2"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")
        logger.info("*************** 搜索账号-一个用户结果检验 ***************")
        userResult_1 = selectUsers(token,{"email":query1["email"]})
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))
        userNum1 = userResult_1.json().get("totalCount")
        userAccount = userResult_1.json().get("users")[0]["email"]
        assert userNum1 == query1["totalCount"]
        assert userAccount == query1["email"]
        logger.info("搜索账号-一个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))
        logger.info("搜索账号-一个用户结果userAccount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["email"], userAccount))

        logger.info("*************** 搜索账号-无结果检验 ***************")
        userResult_2 = selectUsers(token, {"email": query2["email"]})
        assert userResult_2.json().get("result") == except_result
        assert except_msg in userResult_2.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_2.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_2.json().get("message")))
        userNum2 = userResult_2.json().get("totalCount")
        assert userNum2 == query2["totalCount"]
        logger.info("搜索账号-无结果结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["totalCount"], userNum2))

        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("搜索用户状态-状态搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_05(self, testcase_data):
        query1 = testcase_data["query1"]
        query2 = testcase_data["query2"]
        query3 = testcase_data["query3"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")

        logger.info("*************** 使用浏览器登录5个用户（隐藏浏览器登录） ***************")
        step_2()
        logger.info("*************** 状态搜索-默认全部搜索结果检验 ***************")
        userResult_1 = selectUsers(token,"")
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("状态搜索-默认全部搜索结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("状态搜索-默认全部搜索结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))

        userNum1 = userResult_1.json().get("totalCount")
        assert userNum1 == query1["totalCount"]
        logger.info("搜索账号-一个用户结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))

        logger.info("*************** 状态搜索-在线人数搜索结果检验 ***************")
        userResult_2 = selectUsers(token, {"is_online": query2["is_online"]})
        assert userResult_2.json().get("result") == except_result
        assert except_msg in userResult_2.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_2.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_2.json().get("message")))
        userNum2 = userResult_2.json().get("totalCount")
        assert userNum2 == query2["totalCount"]
        logger.info("状态搜索-在线认数搜索结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["totalCount"], userNum2))

        logger.info("*************** 状态搜索-离线人数搜索结果检验 ***************")
        userResult_3 = selectUsers(token, {"is_online": query3["is_online"]})
        assert userResult_3.json().get("result") == except_result
        assert except_msg in userResult_3.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_3.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_3.json().get("message")))
        userNum3 = userResult_3.json().get("totalCount")
        assert userNum3 == query3["totalCount"]
        logger.info("状态搜索-离线人数搜索结果检验totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query3["totalCount"], userNum3))

        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("搜索用户锁定状态-锁定状态搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_06(self, testcase_data):
        query1 = testcase_data["query1"]
        query2 = testcase_data["query2"]
        query3 = testcase_data["query3"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")

        logger.info("*************** 锁定5个用户 ***************")
        step_3(token)
        logger.info("*************** 锁定状态搜索-默认全部搜索结果检验 ***************")
        userResult_1 = selectUsers(token,"")
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("锁定状态搜索-默认全部搜索结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("锁定状态搜索-默认全部搜索结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))

        userNum1 = userResult_1.json().get("totalCount")
        assert userNum1 == query1["totalCount"]
        logger.info("锁定状态搜索-默认全部搜索结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))

        logger.info("*************** 锁定状态搜索-锁定人数搜索结果检验 ***************")
        userResult_2 = selectUsers(token, {"is_locked": query2["is_locked"]})
        assert userResult_2.json().get("result") == except_result
        assert except_msg in userResult_2.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_2.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_2.json().get("message")))
        userNum2 = userResult_2.json().get("totalCount")
        assert userNum2 == query2["totalCount"]
        logger.info("锁定状态搜索-锁定人数搜索结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query2["totalCount"], userNum2))

        logger.info("*************** 非锁定状态搜索-非锁定人数搜索结果检验 ***************")
        userResult_3 = selectUsers(token, {"is_locked": query3["is_locked"]})
        assert userResult_3.json().get("result") == except_result
        assert except_msg in userResult_3.json().get("message")
        logger.info("搜索用户结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_3.json().get("result")))
        logger.info("搜索用户结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_3.json().get("message")))
        userNum3 = userResult_3.json().get("totalCount")
        assert userNum3 == query3["totalCount"]
        logger.info("非锁定状态搜索-非锁定人数搜索结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query3["totalCount"], userNum3))

        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--新用户创建--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("全参数搜索-姓名-账号-邮箱-在线-非锁定状态搜索--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("create_user")  # 执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_select_user_07(self, testcase_data):
        query1 = testcase_data["query1"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 开始执行用例 ***************")
        logger.info("*************** 使用浏览器登录5个用户（隐藏浏览器登录） ***************")
        step_2()
        logger.info("*************** 全参数搜索-姓名-账号-邮箱-在线-非锁定状态搜索结果检验 ***************")
        userResult_1 = selectUsers(token,{"name":query1["name"],"account":query1["account"],"email":query1["email"],"is_online":query1["is_online"],"is_locked":query1["is_locked"]})
        assert userResult_1.json().get("result") == except_result
        assert except_msg in userResult_1.json().get("message")
        logger.info("全参数搜索-姓名-账号-邮箱-在线-非锁定状态搜索结果result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, userResult_1.json().get("result")))
        logger.info("全参数搜索-姓名-账号-邮箱-在线-非锁定状态搜索结果message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, userResult_1.json().get("message")))

        userNum1 = userResult_1.json().get("totalCount")
        userName = userResult_1.json().get("users")[0]["name"]
        userAccount = userResult_1.json().get("users")[0]["account"]
        userEmail = userResult_1.json().get("users")[0]["email"]

        assert userNum1 == query1["totalCount"]
        assert userName == query1["name"]
        assert userAccount == query1["account"]
        assert userEmail == query1["email"]
        logger.info("全参数搜索-姓名-账号-邮箱-在线-非锁定状态搜索结果totalCount ==>> 期望结果：{}， 实际结果：【 {} 】".format(query1["totalCount"], userNum1))
        logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_07_raysync_select_user.py"])