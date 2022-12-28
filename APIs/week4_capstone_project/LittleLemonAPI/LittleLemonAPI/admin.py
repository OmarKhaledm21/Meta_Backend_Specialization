from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','slug')
    
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id','title','category')

admin.site.register(Category,CategoryAdmin)
admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
