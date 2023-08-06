# encoding: utf-8
"""
@project: djangoModel->group_service
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 用户组（部门服务）
@created_time: 2022/9/5 11:33
"""

from django.core.paginator import Paginator

from xj_role.services.role_service import RoleService
from xj_user.services.user_service import UserService
from ..models import UserToGroup, RoleUserGroup
from ..utils.model_handle import format_params_handle, parse_json


# 用户组 树状数据返回
class GroupTreeService(object):
    @staticmethod
    def getTree(data_list, parent_group):
        tree = []
        for item in data_list:
            if str(item['parent_group_id']) == str(parent_group):
                item['children'] = GroupTreeService.getTree(data_list, item['id'])
                tree.append(item)
        return tree

    @staticmethod
    def getTrees(data_list, parent_group):
        tree = []
        if parent_group != 0:
            base_node = RoleUserGroup.objects.filter(id=parent_group).to_json()
            for item in data_list:
                if str(item['parent_group_id']) == str(parent_group):
                    item['children'] = GroupTreeService.getTree(data_list, item['id'])
                    tree.append(item)
            base_node[0]['children'] = tree
            return base_node[0]
        else:
            # 默认不需要搜索
            for item in data_list:
                if not str(item['parent_group_id']) == str(parent_group):
                    continue
                child = GroupTreeService.getTree(data_list, item['id'])
                item['children'] = child
                tree.append(item)
        return tree

    @staticmethod
    def group_tree(group_id=0):
        data_list = RoleUserGroup.objects.filter().to_json()
        group_tree = GroupTreeService.getTrees(data_list, group_id)
        return group_tree, None


# 用户组CURD服务
class GroupService(object):
    @staticmethod
    def get_user_from_group(group_id):
        """根据用户组ID获取用户ID列表"""
        user_obj = UserToGroup.objects.filter(user_group_id=group_id)
        user_list = []
        if user_obj:
            user_list = user_obj.values("user_id")
            user_list = [i['user_id'] for i in user_list]
        return user_list, None

    @staticmethod
    def group_tree_role(params):
        # 分组角色树
        group_id = params.get("group_id", 0)
        tree_data, err = GroupTreeService.group_tree(group_id)
        if err:
            return None, err

        def parse_tree(tree):
            for item in tree:
                data, err = RoleService.get_role_list({"user_group_id": item['id']}, False)
                item['role_list'] = data
                parse_tree(item['children'])
            return tree

        tree_data = parse_json(tree_data)
        tree = parse_tree(tree_data)
        return tree, None

    @staticmethod
    def group_tree_user(params):
        # 分组用户树
        group_id = params.get("group_id", 0)
        tree_data, err = GroupTreeService.group_tree(group_id)
        if err:
            return None, err

        def parse_tree(tree):
            for item in tree:
                user_ids = UserToGroup.objects.filter(user_group=item['id'])
                user_ids = [item["user_id"] for item in list(user_ids.values("user_id"))] if user_ids else []
                item['user_list'] = UserService.user_list(None, user_ids)
                parse_tree(item['children'])
            return tree

        tree_data = parse_json(tree_data)
        tree = parse_tree(tree_data)
        return tree, None

    @staticmethod
    def user_bind_group(user_id, group_id):
        # 用户绑定部门
        if not user_id or not group_id:
            return None, "参数错误，user_id, group_id 必传"
        try:
            UserToGroup.objects.get_or_create(
                {"user_id": user_id, "group_id": group_id},
                user_id=user_id,
                group_id=group_id,
            )
            return None, None
        except Exception as e:
            return None, str(e)

    @staticmethod
    def group_list(params):
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=["page", "size", "group", "group_name", "parent_group_id"],
            alias_dict={"group_name": "group_name__contains"}
        )
        page = params.pop("page", 1)
        size = params.pop("size", 20)
        group_set = RoleUserGroup.objects.filter(**params).values()
        finish_set = list(Paginator(group_set, size).page(page))
        return {"page": int(page), "size": int(size), "list": finish_set}, None

    @staticmethod
    def add_group(params):
        params = format_params_handle(param_dict=params, filter_filed_list=["group", "group_name", "parent_group_id", "description"])
        if not params:
            return None, "参数不能为空"
        instance = RoleUserGroup.objects.create(**params)
        return {"id": instance.id}, None

    @staticmethod
    def edit_group(params):
        params = format_params_handle(param_dict=params, filter_filed_list=["id", "group", "group_name", "parent_group_id", "description"])
        id = params.pop("id", None)
        if not id:
            return None, "ID 不可以为空"
        if not params:
            return None, "没有可以修改的字段"
        instance = RoleUserGroup.objects.filter(id=id)
        if params:
            instance.update(**params)
        return None, None

    @staticmethod
    def del_group(id):
        if not id:
            return None, "ID 不可以为空"
        instance = RoleUserGroup.objects.filter(id=id)
        if instance:
            instance.delete()
        return None, None
