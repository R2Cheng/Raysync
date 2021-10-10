import pytest
import allure
from operation.admin_api import *
from common.logger import logger


@allure.step("获取token")
def step_1():
    respone = admin_login("admin","Test!123")
    logger.info("先获取token")
    return respone.json().get("token")



@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：更改密码-登录")
class TestUpdata():

    @allure.story("用例--更改密码/登录/查看--预期成功")
    @allure.description("该用例是针对 更改密码/登录/查看 场景的测试")
    @allure.title("密码修改成功-预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("initAdmin")#执行用例前可以进行前置操作
    def test_raysync_update_admin_01(self, testcase_data):
        oldpasswd = testcase_data["oldpasswd"]
        newpasswd = testcase_data["newpasswd"]
        oldaccount = testcase_data["oldaccount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        result = admin_updateadmin(token,oldaccount,oldpasswd,newpasswd)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        result1 = admin_login(oldaccount,newpasswd)
        assert result1.json().get("result") == except_result
        assert except_msg in result1.json().get("message")
        result2 = selectAdmin(result1.json().get("token"))
        assert result2.json().get("admin")["account"] == oldaccount
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result2.json().get("result")))
        logger.info("登录结果 ==>> 期望结果：{}， 实际结果：【 {} 】".format(oldaccount, result2.json().get("admin")["account"]))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--更改密码/登录/查看--预期失败")
    @allure.description("该用例是针对 更改密码/登录/查看 场景的测试")
    @allure.title("密码更改不符合要求-预期失败")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("initAdmin")#执行用例前可以进行前置操作
    def test_raysync_update_admin_02(self, testcase_data):
        oldpasswd = testcase_data["oldpasswd"]
        errorpasswd = testcase_data["errorpasswd"]
        oldaccount = testcase_data["oldaccount"]
        except_result = testcase_data["except_result"]
        except_result1 = testcase_data["except_result1"]
        except_msg1 = testcase_data["except_msg1"]
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        result = admin_updateadmin(token,oldaccount,oldpasswd,errorpasswd)
        assert result.json().get("result") == except_result1
        assert except_msg1 in result.json().get("message")
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("修改结果 ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg1, result.json().get("message")))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--更改密码/登录/查看--预期失败")
    @allure.description("该用例是针对 更改密码/登录/查看 场景的测试")
    @allure.title("旧密码输入错误-预期失败")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("initAdmin")#执行用例前可以进行前置操作
    def test_raysync_update_admin_03(self, testcase_data):
        oldpasswd = testcase_data["oldpasswd"]
        newpasswd = testcase_data["newpasswd"]
        errorpasswd = testcase_data["errorpasswd"]
        oldaccount = testcase_data["oldaccount"]
        newaccount = testcase_data["newaccount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        result = admin_updateadmin(token,oldaccount,errorpasswd,newpasswd)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("修改结果 ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result.json().get("message")))
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--更改密码/登录/查看--预期成功")
    @allure.description("该用例是针对 更改密码/登录/查看 场景的测试")
    @allure.title("账号修改-预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("initAdmin")#执行用例前可以进行前置操作
    def test_raysync_update_admin_04(self, testcase_data):
        oldpasswd = testcase_data["oldpasswd"]
        newpasswd = testcase_data["newpasswd"]
        oldaccount = testcase_data["oldaccount"]
        newaccount = testcase_data["newaccount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 开始执行用例 ***************")
        token = step_1()
        result = admin_updateadmin(token,newaccount,oldpasswd,newpasswd)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        result1 = admin_login(newaccount,newpasswd)
        assert result1.json().get("result") == except_result
        assert except_msg in result1.json().get("message")
        result2 = selectAdmin(result1.json().get("token"))
        assert result2.json().get("admin")["account"] == newaccount
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result2.json().get("result")))
        logger.info("登录结果 ==>> 期望结果：{}， 实际结果：【 {} 】".format(newaccount, result2.json().get("admin")["account"]))
        logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_02_raysync_updata_admin.py"])