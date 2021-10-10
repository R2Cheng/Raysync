import pytest
import allure
from operation.admin_api import *
from common.logger import logger
from common.raysync_rayfile_c import rayfile_c


@allure.step("获取token")
def step_1():
    respone = admin_login("admin","Test!123")
    logger.info("先获取token")
    return respone.json().get("token")

@allure.step("执行命令行传输任务")
def step_2(status,sessions_num):
    if status:
        rayfile_c(sessions_num)
    else:
        pass


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：正在传输任务")
class TestSession():

    @allure.story("用例--无传输任务-列表为空--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("无传输任务-列表为空--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作
    def test_raysync_session_01(self, testcase_data):
        status = testcase_data["status"]
        sessions_num = testcase_data["sessions_num"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行命令行传输任务 ***************")
        step_2(status,sessions_num)
        logger.info("*************** 开始执行用例 ***************")
        result = sessions(token)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        assert len(result.json().get("sessions")) == sessions_num
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result.json().get("message")))
        logger.info("传输任务列表数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(sessions_num, len(result.json().get("sessions"))))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--有传输任务-单任务传输--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("无传输任务-列表为空--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("remove_all")#执行用例前可以进行前置操作
    def test_raysync_session_02(self, testcase_data):
        status = testcase_data["status"]
        sessions_num = testcase_data["sessions_num"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行命令行传输任务 ***************")
        step_2(status,sessions_num)
        logger.info("*************** 开始执行用例 ***************")
        result = sessions(token)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        assert len(result.json().get("sessions")) == sessions_num
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result.json().get("message")))
        logger.info("传输任务列表数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(sessions_num, len(result.json().get("sessions"))))
        sessions_num_now = len(result.json().get("sessions"))
        for i in range(0,sessions_num_now):
            taskname = result.json().get("sessions")[i]["taskname"]
            result1 = stopTask(token,taskname)
            assert result1.json().get("result") == 0
            assert "OK" in result1.json().get("message")
            logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result1.json().get("result")))
            logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result1.json().get("message")))
            logger.info("*************** 停止任务{}成功 ***************".format(taskname))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--有传输任务-多任务传输--预期成功")
    @allure.description("该用该用例是针对业务场景的测试")
    @allure.title("无传输任务-列表为空--预期成功")
    @pytest.mark.multiple
    @pytest.mark.usefixtures("remove_all")#执行用例前可以进行前置操作
    def test_raysync_session_03(self, testcase_data):
        status = testcase_data["status"]
        sessions_num = testcase_data["sessions_num"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行命令行传输任务 ***************")
        step_2(status,sessions_num)
        logger.info("*************** 开始执行用例 ***************")
        result = sessions(token)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        assert len(result.json().get("sessions")) == sessions_num
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result.json().get("message")))
        logger.info("传输任务列表数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(sessions_num, len(result.json().get("sessions"))))
        sessions_num_now = len(result.json().get("sessions"))
        for i in range(0, sessions_num_now):
            taskname = result.json().get("sessions")[i]["taskname"]
            result1 = stopTask(token, taskname)
            assert result1.json().get("result") == 0
            assert "OK" in result1.json().get("message")
            logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result1.json().get("result")))
            logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format("OK", result1.json().get("message")))
            logger.info("*************** 停止任务{}成功 ***************".format(taskname))
        logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_03_raysync_session.py"])