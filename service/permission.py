from django.conf import settings
from collections import OrderedDict
def init_permission(user_object,request):
    """
    权限信息初始化，将权限信息放入session
    :return:
    """
    # 用户正确
    # 1. 获取用户拥有的权限信息
    # 1.1 获取用户拥有的所有角色对象
    # user_object.roles.all()
    # 1.2 django连表 + 去重 + 空值的判断
    permission_list = user_object.roles.filter(permissions__title__isnull=False).values('permissions__title',
                                                                                        'permissions__url',
                                                                                        'permissions__name',
                                                                                        'permissions__menu_id',
                                                                                        'permissions__menu__title',
                                                                                        'permissions__menu__icon',
                                                                                        'permissions__parent__name',
                                                                                        ).distinct()


    # 2. 对权限信息进行结构处理
    permission_dict = {}
    menu_list = []

    for item in permission_list:
        if item['permissions__menu_id']:
            menu_list.append({
                'title':item['permissions__title'],
                'url':item['permissions__url'],
                'name':item['permissions__name'],
                'menu_id':item['permissions__menu_id'],
                'menu_title':item['permissions__menu__title'],
                'menu_icon':item['permissions__menu__icon'],
            })
        permission_dict[item['permissions__name']] = {
            'url': item['permissions__url'],
            'parent_name':item['permissions__parent__name'],
            'title':item['permissions__title']
        }

    menu_dict = OrderedDict()
    for item in menu_list:
        menu_id = item['menu_id']
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append({'title': item['title'], 'url': item['url'],
                                                   'name': item['name']})
        else:
            menu_dict[menu_id] = {
                'id': menu_id,
                'title': item['menu_title'],
                'icon': item['menu_icon'],
                'class':'hide',
                'children': [
                    {'title': item['title'], 'url': item['url'],
                     'name': item['name']}
                ]
            }

    """
    {
        depart_list:{'url':'/depart/list/' },
        depart_list:{'url':'/depart/list/' },
        depart_list:{'url':'/depart/list/' },
        depart_list:{'url':'/depart/list/' },
    }
    """
    # 3. 放入session
    request.session[settings.RBAC_SESSION_PERMISSION_KEY] = permission_dict
    request.session[settings.RBAC_SESSION_MENU_KEY] = list(menu_dict.values())