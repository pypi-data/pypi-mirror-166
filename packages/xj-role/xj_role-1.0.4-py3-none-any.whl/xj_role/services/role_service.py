# encoding: utf-8
"""
@project: djangoModel->role_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 角色服务
@created_time: 2022/9/2 15:37
"""
from django.core.paginator import Paginator

from xj_role.models import Role
from ..utils.model_handle import format_params_handle


class RoleService:
    @staticmethod
    def get_role_list(params):
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        params = format_params_handle(param_dict=params, filter_filed_list=["id", "permission_id", "role", "user_group_id", "page", "size"])
        query_set = Role.objects.filter(**params).values()
        finish_set = list(Paginator(query_set, size).page(page).object_list)
        return finish_set, None

    @staticmethod
    def role_tree(role_ids=None):
        # 获取子角色： 获取当前等级角色
        current_info = Role.objects.filter(id__in=role_ids) if role_ids else Role.objects.filter(parent_role_id=0)
        if not current_info:
            return [], None
        base_info_list = list(current_info.values())
        for base_info in base_info_list:
            base_info.setdefault("child", RoleService.tree_loop(base_info['id']))
        return base_info_list, None

    @staticmethod
    def tree_loop(role_id=0):
        tem_set = tree_list = list(Role.objects.filter(parent_role_id=role_id).values())
        for index, value in enumerate(tem_set):
            tree_list[index].setdefault("child", RoleService.tree_loop(value['id']))
        return tree_list
