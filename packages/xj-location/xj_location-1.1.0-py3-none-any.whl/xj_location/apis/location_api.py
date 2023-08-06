# encoding: utf-8
"""
@project: djangoModel->location_api
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis:
@created_time: 2022/9/7 13:27
"""

# ================ 定位操作 =====================
from rest_framework.views import APIView

from ..services.location_service import LocationService
from ..utils.model_handle import *


class LocationAPI(APIView):
    def list(self, **kwargs):
        # 用户组 列表接口
        params = parse_data(self)
        data, err = LocationService.location_list(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    def put(self, request, **kwargs):
        # 用户组 编辑接口
        params = parse_data(request)
        params.setdefault("id", kwargs.get("id", None))
        data, err = LocationService.edit_location(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    def post(self, request, **kwargs):
        # 用户组 添加接口
        params = parse_data(request)
        data, err = LocationService.add_location(params)
        if err:
            return util_response(err=1000, msg=err)
        return util_response(data=data)

    def delete(self, request, **kwargs):
        # 用户组 删除接口
        id = parse_data(request).get("id", None) or kwargs.get("id")
        if not id:
            return util_response(err=1000, msg="id 必传")
        data, err = LocationService.del_location(id)
        if err:
            return util_response(err=1001, msg=err)
        return util_response(data=data)

    def test(self):
        # 测试接口
        params = {"thread_id_list": [1, 2]}
        data, err = LocationService.location_list(params, False)
        return util_response(data=data)
