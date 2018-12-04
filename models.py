from django.db import models

class Menu(models.Model):
    """
    菜单表
    """
    title = models.CharField(verbose_name='菜单',max_length=32)
    icon = models.CharField(verbose_name='图标',max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '菜单表'


class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(verbose_name='名称',max_length=32)
    name = models.CharField(verbose_name='URL别名',max_length=32,unique=True)
    url = models.CharField(verbose_name='URL',max_length=32)
    menu = models.ForeignKey(verbose_name='菜单',to='Menu',null=True,blank=True)

    parent = models.ForeignKey(verbose_name='父权限',to="Permission",null=True,blank=True)

    class Meta:
        verbose_name_plural = '权限表'

    def __str__(self):
        return self.title

class Role(models.Model):
    """
    角色表
    """
    title = models.CharField(verbose_name='名称',max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的权限',to='Permission',blank=True)

    class Meta:
        verbose_name_plural = '角色表'

    def __str__(self):
        return self.title

class AbstractUserInfo(models.Model):
    """
    用户表
    """
    username = models.CharField(verbose_name='用户名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    roles = models.ManyToManyField(verbose_name='拥有的角色',to=Role)

    class Meta:
        abstract = True # 当前类不会再数据库迁移时候生成相关的表了，他来当 “基类”，给业务表中的用户表使用


