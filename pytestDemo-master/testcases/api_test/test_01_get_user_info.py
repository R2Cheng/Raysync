import pytest
import allure
from operation.admin_api import *
from testcases.conftest import api_data
from common.logger import logger


@allure.step("步骤1 ==>> 获取token")
def step_1():
    respone = admin_login("admin","Test!123")
    logger.info("步骤1 ==>> 获取token")
    return respone.json().get("token")


@allure.step("步骤1 ==>> 获取某个用户信息")
def step_2(username):
    logger.info("步骤1 ==>> 获取某个用户信息：{}".format(username))


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic("针对单个接口的测试")
@allure.feature("镭速后管接口")
class TestRaysync_admin_api_test():
    """镭速软件后管单一接口测试"""


    @allure.story("用例--登录测试")
    @allure.description("该用例是针对登录接口的测试")
    @pytest.mark.single
    @pytest.mark.parametrize("account,password,result, message",
                             api_data["login"])
    def test_login(self,account,password, result, message):
        logger.info("*************** 开始执行用例 ***************")
        #step_1()
        respone = admin_login(account,password)
        assert respone.json().get("result") == result
        logger.info("result ==>> 期望结果：{}， 实际结果：{}".format(result, respone.json().get("result")))
        assert message in respone.json().get("message")
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--登出测试")
    @allure.description("该用例是针对登录接口的测试")
    @pytest.mark.single
    @pytest.mark.parametrize("token,result, message",api_data["logout"])
    def test_logout(self,token,result,message):
        logger.info("*************** 开始执行用例 ***************")
        if token == "":
            pass
        elif token == "正常获取":
            token = step_1()
        respone = admin_logout(token)
        assert respone.json().get("result") == result
        logger.info("result ==>> 期望结果：{}， 实际结果：{}".format(result, respone.json().get("result")))
        assert message in respone.json().get("message")
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--更新当前管理员信息")
    @allure.description("该用例是针对登录接口的测试")
    @pytest.mark.single
    @pytest.mark.parametrize("oldPassword,newPassword, result,message", api_data["UPDATE_ADMIN"])
    def test_updataadmin(self,oldPassword,newPassword,result,message):
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        respone = admin_updateadmin(token,"admin",oldPassword,newPassword)
        assert respone.json().get("result") == result
        logger.info("result ==>> 期望结果：{}， 实际结果：{}".format(result, respone.json().get("result")))
        assert message in respone.json().get("message")
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--更新服务器信息")
    @allure.description("该用例是针对登录接口的测试")
    @pytest.mark.skip(reason="执行之后存在前台登录错误的问题，暂不处理")
    @pytest.mark.single
    @pytest.mark.parametrize("name,host,proxyPort,packageSize,outbounde,compression,license,result, message", api_data["UPDATE_SERVER"])
    def test_admin_upadteserver(self,name,host,proxyPort,packageSize,outbounde,compression,license,result, message):
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        respone = admin_upadteserver(token,name,host,proxyPort,packageSize,outbounde,compression,license)
        assert respone.json().get("result") == result
        logger.info("result ==>> 期望结果：{}， 实际结果：{}".format(result, respone.json().get("result")))
        assert message in respone.json().get("message")
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--空间统计")
    @allure.description("该用例是针对空间统计的测试")
    @pytest.mark.single
    @pytest.mark.parametrize("time,result,message", api_data["SET_USER_HOME_COUNT_PERIOD"])
    def test_updataadmin(self,time,result,message):
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        respone = setUserHomeCountPeriod(token,time)
        assert respone.json().get("result") == result
        logger.info("result ==>> 期望结果：{}， 实际结果：{}".format(result, respone.json().get("result")))
        assert message in respone.json().get("message")
        logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_get_user_info.py"])
