from django.contrib import admin
from rbac import models

class MenuAdmin(admin.ModelAdmin):
    list_display = ['title','icon']
admin.site.register(models.Menu,MenuAdmin)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title','url','name','menu','parent']
admin.site.register(models.Permission,PermissionAdmin)


admin.site.register(models.Role)
