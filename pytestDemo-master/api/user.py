import os
from core.rest_client import RestClient
from common.read_data import data

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
api_root_url = data.load_ini(data_file_path)["host"]["api_root_url"]
api_fe_url = data.load_ini(data_file_path)["host"]["api_fe_url"]


class Raysync(RestClient):

    def __init__(self, api_root_url, **kwargs):
        super(Raysync, self).__init__(api_root_url, **kwargs)

    def raysync_request(self, **kwargs):
        return self.post("/admin/api", **kwargs)

    def raysync_request_setlogo(self,**kwargs):
        return self.post("/admin/setlogo",**kwargs)

    def raysync_fe_request(self,**kwargs):
        return self.post("/api",**kwargs)

    def raysync_fe_login_request(self,**kwargs):
        return self.post("/rayfile", **kwargs)


raysync = Raysync(api_root_url)
raysync_fe = Raysync(api_fe_url)