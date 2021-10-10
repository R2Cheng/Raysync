import pytest
import os
import allure
from api.user import raysync
from operation.admin_api import *
from common.mysql_operate import db
from common.read_data import data
from common.logger import logger
from common.raysync_rayfile_c import rayfile_c_remove_all

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(BASE_PATH, "data", yaml_file_name)
        yaml_data = data.load_yaml(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


base_data = get_data("base_data.yml")
api_data = get_data("api_test_data.yml")
scenario_data = get_data("scenario_test_data.yml")


@allure.step("前置步骤 ==>> 清理数据")
def step_first():
    logger.info("******************************")
    logger.info("前置步骤开始 ==>> 清理数据")


@allure.step("后置步骤 ==>> 清理数据")
def step_last():
    logger.info("后置步骤开始 ==>> 清理数据")


@allure.step("前置步骤 ==>> 管理员用户登录")
def step_login(username, password):
    logger.info("前置步骤 ==>> 管理员 {} 登录，返回信息 为：{}".format(username, password))


@pytest.fixture(scope="session")
def login_fixture():
    username = base_data["init_admin_user"]["username"]
    password = base_data["init_admin_user"]["password"]
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "username": username,
        "password": password
    }
    loginInfo = user.login(data=payload, headers=header)
    step_login(username, password)
    yield loginInfo.json()

@pytest.fixture(scope="function")
def initAdmin():
    '''修改admin账户，先恢复默认账户的密码'''
    update_sql = base_data["init_sql"]["initadmin"]
    db.execute_db(update_sql)
    step_first()
    logger.info("修改admin账户，恢复默认账号密码")
    logger.info("执行前置SQL：{}".format(update_sql))

@pytest.fixture(scope="function")
def remove_all():
    '''清空用户文件列表'''
    rayfile_c_remove_all()

@pytest.fixture(scope="function")
def insert_delete_user():
    """删除用户前，先在数据库插入一条用户数据"""
    insert_sql = base_data["init_sql"]["insert_delete_user"][0]
    db.execute_db(insert_sql)
    step_first()
    logger.info("删除用户操作：插入新用户--准备用于删除用户")
    logger.info("执行前置SQL：{}".format(insert_sql))
    yield
    # 因为有些情况是不给删除管理员用户的，这种情况需要手动清理上面插入的数据
    del_sql = base_data["init_sql"]["insert_delete_user"][1]
    db.execute_db(del_sql)
    step_last()
    logger.info("删除用户操作：手工清理处理失败的数据")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def delete_register_user():
    """注册用户前，先删除数据，用例执行之后，再次删除以清理数据"""
    del_sql = base_data["init_sql"]["delete_register_user"]
    db.execute_db(del_sql)
    step_first()
    logger.info("注册用户操作：清理用户--准备注册新用户")
    logger.info("执行前置SQL：{}".format(del_sql))
    yield
    db.execute_db(del_sql)
    step_last()
    logger.info("注册用户操作：删除注册的用户")
    logger.info("执行后置SQL：{}".format(del_sql))


@pytest.fixture(scope="function")
def create_user():
    user_list = ["镭速,leisu1,leisu_test_1@email.com",
                "镭速,leisu2,leisu_test_2@email.com",
                "镭速,leisu3,leisu_test_3@email.com",
                "镭速,leisu4,leisu_test_4@email.com",
                "镭速测试,leisu5,leisu_test_5@email.com",
                "raysync_test,raysync_test_1,raysync_test_1@email.com",
                "raysync_test,raysync_test_2,raysync_test_2@email.com",
                "raysync_test,raysync_test_3,raysync_test_3@email.com",
                "raysync_test,raysync_test_4,raysync_test_4@email.com",
                "raysync_test_1,raysync_test_5,raysync_test_5@email.com",
                "raysync_test_10,raysync_test_10,raysync_test_10@email.com",
                "raysync_test_11,raysync_test_11,raysync_test_11@email.com",
                "raysync_test_12,raysync_test_12,raysync_test_12@email.com",
                "raysync_test_13,raysync_test_13,raysync_test_13@email.com",
                "raysync_test_14,raysync_test_14,raysync_test_14@email.com",
                "raysync_test_15,raysync_test_15,raysync_test_15@email.com",
                ]
    respone = admin_login("admin", "Test!123")
    token = respone.json().get("token")
    #先删除所有用户
    while True:
        user = []
        r = selectUsers(token,query="")
        if len(r.json().get("users")) == 0:
            break
        for i in r.json().get("users"):
            user_id = i["id"]
            user.append(user_id)
        deleteUsers(token,user)
    if len(r.json().get("users")) == 0:
        for i in user_list:
            name,account,email = i.split(",")[0],i.split(",")[1],i.split(",")[2]
            admin_createuser(token=token,account=account,passwd="Test!123",name=name,needUpdatePwd=0,email=email)