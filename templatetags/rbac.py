import re
from django.template import Library
from django.conf import settings

register = Library()

# 用于在为模板自定义函数，调用方式： {% func 1 2 3 4 %}
@register.simple_tag
def func(a1,a2,a3,a4):
    return a1 + "666"

# 用于在为模板自定义函数，调用方式： {{ '田建宇'|foo:"dsb" }} + 可以在 if后面做条件
@register.filter
def foo(a1,a2):
    return '999'

# 用于返回一个代码块
@register.inclusion_tag('rbac/menu.html')
def get_menu(request):
    menu_list = request.session.get(settings.RBAC_SESSION_MENU_KEY)
    """
    [
        {
            id:1,
            title:'父菜单1',
            'class':'',
            children:[
                {'id':1,'title':'部门列表','url':...},
                {'id':5,'title':'用户列表','url':...},
            ]
            
        },
        {
            id:2,
            title:'父菜单2',
            'class':'hide',
            children:[
                {'id':1,'title':'订单列表','url':...},
            ]
            
        }
    ]
    """
    for menu in menu_list:
        for child in menu['children']:
            if child['name'] == getattr(request,settings.RBAC_CURRENT_PARENT_NAME,None):
                menu['class'] = ""
                child['class'] = 'active'

    return {
        'menu_list': menu_list
    }

@register.inclusion_tag('rbac/breadcrumb.html')
def get_breadcrumb(request):
    record_list = getattr(request,settings.RBAC_RECORD_LIST)
    return {'record_list':record_list}

@register.filter
def has_permission(request,name):
    """
    判断用户是否有该name权限
    :param request:
    :param name:
    :return:
    """
    permission_dict = request.session.get(settings.RBAC_SESSION_PERMISSION_KEY)
    if name in permission_dict:
        return True
