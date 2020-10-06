from django.contrib import admin

# Register your models here.

# From inside your project's urls.py file
from django.urls import path, include
from django.contrib import admin
# THIS SECTION IS NEW!
# ********************
from store_app.models import User as U, Product, ShippingOrder, BigBanner, SmallBanner, UserOrder, Order, OrderItem

class UAdmin(admin.ModelAdmin):
    pass
admin.site.register(U, UAdmin)
########################################
class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order, OrderAdmin)
#########################################
class OrderItemAdmin(admin.ModelAdmin):
    pass
admin.site.register(OrderItem, OrderItemAdmin)
#########################################
class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)
################################################
class ShippingOrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(ShippingOrder, ShippingOrderAdmin)
################################################
class BigBannerAdmin(admin.ModelAdmin):
    pass
admin.site.register(BigBanner, BigBannerAdmin)
################################################
class SmallBannerAdmin(admin.ModelAdmin):
    pass
admin.site.register(SmallBanner, SmallBannerAdmin)
################################################
class UserOrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(UserOrder, UserOrderAdmin)


