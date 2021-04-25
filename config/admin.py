from django.contrib import admin

from typeidea.base_admin import BaseOwnerAdmin
from typeidea.custom_site import custom_site
from .models import Link
from .models import SiderBar
# Register your models here.


@admin.register(Link, site=custom_site)
class LinkAdmin(BaseOwnerAdmin):
    # 需要后台显示的model里的列表字段
    list_display = ("title", "href", "status", "weight", "create_time")
    # 需要后台操作的model里的列表字段
    fields = ("title", "href", "status", "weight")


@admin.register(SiderBar, site=custom_site)
class SiderBarAdmin(BaseOwnerAdmin):
    # 需要后台显示的model里的列表字段
    list_display = ("title", "display_type", "content", "create_time")
    # 需要后台操作的model里的列表字段
    fields = ("title", "display_type", "content")

    # 保存model方法，owner字段获取当前请求的用户名，重新调用自己保存
    # def save_model(self, request, obj, form, change):
    #     obj.owner = request.user
    #     return super(SiderBarAdmin, self).save_model(request, obj, form, change)

