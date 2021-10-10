import pytest
import allure
from operation.admin_api import *
from operation.fe_api import *
from common.logger import logger
from common.raysync_rayfile_c import rayfile_c


@allure.step("获取token")
def step_1():
    respone = admin_login("admin","Test!123")
    logger.info("先获取token")
    return respone.json().get("token")

@allure.step("执行清空邀请上传链接操作")
def step_2(token,stime,etime):
    url = []
    response = getAllShareLink(token,stime,etime)
    totalCount = response.json().get("totalCount")
    if totalCount !=0:
        while True:
            for i in response.json().get("sharelinkinfo"):
                url.append(i["shareLink"])
            delShareLink(token,url)
            url.clear()
            response = getAllShareLink(token, stime, etime)
            totalCount = response.json().get("totalCount")
            if totalCount == 0:
                break

@allure.step("执行链接数据初始化操作")
def step_3():
    logger.info("获取前台登录token，userId")
    result= feLogin("test1","Test!123")
    token = result.json().get("token")
    userId = result.json().get("userId")
    logger.info("创建邀请上传链接")
    createUrl(token,userId)
    createUrl(token,userId,expireTime=1)
    createUrl(token, userId, expireTime=3)
    createUrl(token, userId, expireTime=7)
    createUrl(token, userId, expireTime=30)
    createUrl(token, userId, expireTime=-1)


@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("针对业务场景的测试")
@allure.feature("场景：邀请上传")
class TestshareLink():

    @allure.story("用例--查看邀请上传链接列表--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("查看邀请上传链接列表-列表为空--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_sharelink_01(self, testcase_data):
        stime = testcase_data["stime"]
        etime = testcase_data["etime"]
        totalCount = testcase_data["totalCount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行清空邀请上传链接操作 ***************")
        step_2(token,stime,etime)
        logger.info("*************** 开始执行用例 ***************")
        result = getAllShareLink(token,stime,etime)
        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        assert result.json().get("totalCount") == totalCount
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result.json().get("message")))
        logger.info("邀请上传链接数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(totalCount, result.json().get("totalCount")))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--查看邀请上传链接列表--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("查看邀请上传链接列表-列表不为空，共6条链接（5条使用中（永久，1天，3天，7天，30天），默认参数（无需邮件通知），1条过期）,有效链接验证通过--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_sharelink_02(self, testcase_data):
        stime = testcase_data["stime"]
        etime = testcase_data["etime"]
        useCount = testcase_data["useCount"]
        overCount = testcase_data["overCount"]
        totalCount = testcase_data["totalCount"]
        cancelCount = testcase_data["cancelCount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行清空邀请上传链接操作 ***************")
        step_2(token,stime,etime)
        logger.info("*************** 执行邀请上传链接数据初始化操作 ***************")
        step_3()
        logger.info("*************** 开始执行用例 ***************")
        result = getAllShareLink(token,stime,etime)
        useCountNum = 0
        overCountNum = 0
        cancelCountNum = 0
        for sharelinkinfo in result.json().get("sharelinkinfo"):
            if sharelinkinfo["shareLinkStatus"] == 1:  #链接有效
                useCountNum += 1
                url = sharelinkinfo["shareLink"]
                passwd = sharelinkinfo["sharePassword"]
                result_url = checkUrl(url)
                result_passwd = checkPasswd(url, passwd)
                assert 0 == result_url.json().get("result")
                assert 0 == result_passwd.json().get("result")
                logger.info("result_url ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_url.json().get("result")))
                logger.info("result_passwd ==>> 期望结果：{}， 实际结果：【 {} 】".format(0, result_passwd.json().get("result")))
            elif sharelinkinfo["shareLinkStatus"] == 2: #链接过期
                overCountNum += 1
                url = sharelinkinfo["shareLink"]
                result_url = checkUrl(url)
                assert 1041 == result_url.json().get("result")
                logger.info("result_url ==>> 期望结果：{}， 实际结果：【 {} 】".format(1041, result_url.json().get("result")))
            else:   #链接取消
                cancelCountNum += 1

        assert result.json().get("result") == except_result
        assert except_msg in result.json().get("message")
        assert result.json().get("totalCount") == totalCount
        assert useCountNum == useCount
        assert overCountNum == overCount
        assert cancelCountNum == cancelCount
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result.json().get("message")))
        logger.info("邀请上传链接数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(totalCount, result.json().get("totalCount")))
        logger.info("邀请上传链接使用中数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(useCount, useCountNum))
        logger.info("邀请上传链接过期数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(overCount, overCountNum))
        logger.info("邀请上传链接取消数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(cancelCount, cancelCountNum))
        logger.info("*************** 结束执行用例 ***************")


    @allure.story("用例--查看邀请上传链接列表--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("查看邀请上传链接列表-列表不为空--使用中和过期链接取消邀请上传成功，并验证url不通过--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_sharelink_03(self, testcase_data):
        stime = testcase_data["stime"]
        etime = testcase_data["etime"]
        useCount = testcase_data["useCount"]
        overCount = testcase_data["overCount"]
        totalCount = testcase_data["totalCount"]
        cancelCount = testcase_data["cancelCount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行清空邀请上传链接操作 ***************")
        step_2(token,stime,etime)
        logger.info("*************** 执行邀请上传链接数据初始化操作 ***************")
        step_3()
        logger.info("*************** 开始执行用例 ***************")
        result_old_url = getAllShareLink(token,stime,etime)
        shareLink = []
        useCountNum = 0
        overCountNum = 0
        cancelCountNum = 0
        for sharelinkinfo in result_old_url.json().get("sharelinkinfo"):
            if sharelinkinfo["shareLinkStatus"] !=3:
                shareLink.append(sharelinkinfo["shareLink"])
                result_disable = disableShareLink(token,shareLink)
                shareLink.clear()
                assert 0 == result_disable.json().get("result")

        result_new_url = getAllShareLink(token,stime,etime)
        for sharelinkinfo in result_new_url.json().get("sharelinkinfo"):
            if sharelinkinfo["shareLinkStatus"] == 1:  # 链接有效
                useCountNum += 1
            elif sharelinkinfo["shareLinkStatus"] == 2: #链接过期
                overCountNum += 1
            else:   #链接取消
                cancelCountNum += 1
                url = sharelinkinfo["shareLink"]
                result_url = checkUrl(url)
                assert 1037 == result_url.json().get("result")
                logger.info("result_url ==>> 期望结果：{}， 实际结果：【 {} 】".format(1037, result_url.json().get("result")))

        assert result_new_url.json().get("result") == except_result
        assert except_msg in result_new_url.json().get("message")
        assert result_new_url.json().get("totalCount") == totalCount
        assert useCountNum == useCount
        assert overCountNum == overCount
        assert cancelCountNum == cancelCount
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_new_url.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_new_url.json().get("message")))
        logger.info("邀请上传链接数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(totalCount, result_new_url.json().get("totalCount")))
        logger.info("邀请上传链接使用中数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(useCount, useCountNum))
        logger.info("邀请上传链接过期数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(overCount, overCountNum))
        logger.info("邀请上传链接取消数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(cancelCount, cancelCountNum))
        logger.info("*************** 结束执行用例 ***************")

    @allure.story("用例--查看邀请上传链接列表--预期成功")
    @allure.description("该用例是针对业务场景的测试")
    @allure.title("查看邀请上传链接列表-列表不为空--删除1个有效链接和1个过期链接--预期成功")
    @pytest.mark.multiple
    # @pytest.mark.usefixtures("")#执行用例前可以进行前置操作(数据库操作,尽量不使用)
    def test_raysync_sharelink_04(self, testcase_data):
        stime = testcase_data["stime"]
        etime = testcase_data["etime"]
        useCount = testcase_data["useCount"]
        overCount = testcase_data["overCount"]
        totalCount = testcase_data["totalCount"]
        cancelCount = testcase_data["cancelCount"]
        except_result = testcase_data["except_result"]
        except_msg = testcase_data["except_msg"]
        logger.info("*************** 获取token ***************")
        token = step_1()
        logger.info("*************** 执行清空邀请上传链接操作 ***************")
        step_2(token, stime, etime)
        logger.info("*************** 执行邀请上传链接数据初始化操作 ***************")
        step_3()
        logger.info("*************** 开始执行用例 ***************")
        result_old_url = getAllShareLink(token,stime,etime)
        useLink = []
        overLink = []
        useCountNum = 0
        overCountNum = 0
        cancelCountNum = 0
        for sharelinkinfo in result_old_url.json().get("sharelinkinfo"):
            if sharelinkinfo["shareLinkStatus"]==1:
                if len(useLink) == 0: #测试用例只需要删除一个
                    useLink.append(sharelinkinfo["shareLink"])
            elif sharelinkinfo["shareLinkStatus"] == 2:
                if len(overLink) == 0:  # 测试用例只需要删除一个
                    overLink.append(sharelinkinfo["shareLink"])
            else:
                pass
        delShareLink(token,useLink)
        delShareLink(token,overLink)
        result_new_url = getAllShareLink(token, stime, etime)
        for sharelinkinfo in result_new_url.json().get("sharelinkinfo"):
            if sharelinkinfo["shareLinkStatus"]==1:
                useCountNum +=1
            elif sharelinkinfo["shareLinkStatus"] == 2:
                overCountNum +=1
            else:
                cancelCountNum +=1
        assert result_new_url.json().get("result") == except_result
        assert except_msg in result_new_url.json().get("message")
        assert result_new_url.json().get("totalCount") == totalCount
        assert useCountNum == useCount
        assert overCountNum == overCount
        assert cancelCountNum == cancelCount
        logger.info("result ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_result, result_new_url.json().get("result")))
        logger.info("message ==>> 期望结果：{}， 实际结果：【 {} 】".format(except_msg, result_new_url.json().get("message")))
        logger.info("邀请上传链接数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(totalCount, result_new_url.json().get("totalCount")))
        logger.info("邀请上传链接使用中数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(useCount, useCountNum))
        logger.info("邀请上传链接过期数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(overCount, overCountNum))
        logger.info("邀请上传链接取消数量 ==>> 期望结果：{}， 实际结果：【 {} 】".format(cancelCount, cancelCountNum))
        logger.info("*************** 结束执行用例 ***************")
if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_04_raysync_sharelink.py"])