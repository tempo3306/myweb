from myweb.wsgi import *
from django.contrib.auth.models import Group, Permission

###初始化论坛用户组
def init_group(role_name):
    try:
        Group.objects.get(name=role_name)
        print("角色组已经存在")
    except Group.DoesNotExist:
        groups = Group.objects.create(name=role_name)
        pers = role_permissions[role_name]
        for per  in pers:
            print(per)
            permission = Permission.objects.get(codename=per)
            groups.permissions.add(permission)



'''
        permissions = (('read', '阅读'),
                       ('reply', '回复'),
                       ('post', '发帖'),
                       ('delete', '删除'),
                       ('control', '控制'))
'''
###定义角色对应的权限
role_permissions = {'forbidden_user': ['read'],
                    'normal_user': ['read', 'reply'],
                    'core_user': ['read', 'reply', 'post'],
                    'moderator': ['read', 'reply', 'post', 'delete'],
                    'admin': ['read', 'reply', 'post', 'delete', 'control']}



if __name__ == '__main__':
    for role, per in role_permissions.items():
        init_group(role)