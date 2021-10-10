import pytest
import allure
from operation.admin_api import *
from common.logger import logger


# @allure.step("xxxxx")
# def step_1():
#     logger.info("xxxxxx")
#

@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：用户登录-查看用户")
class TestRegLogList():

    @allure.story("用例--注册/登录/查看--预期成功")
    @allure.description("该用例是针对 登录-查看 场景的测试")
    @allure.title("用户登录查看-预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作
    def test_raysync_login(self, testcase_data):
        account = testcase_data["account"]
        password = testcase_data["password"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 开始执行用例 ***************")
        result = admin_login(account, password)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        result1 = selectAdmin(result.json().get("token"))
        assert result1.json().get("result") == except_result
        assert except_msg in result1.json().get("message")
        assert result1.json().get("admin")["account"] == account
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result1.json().get("result")))
        logger.info("登录结果 ==>> 期望结果：{}， 实际结果：【 {} 】".format(account, result1.json().get("admin")["account"]))
        logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_01_raysync_login.py"])