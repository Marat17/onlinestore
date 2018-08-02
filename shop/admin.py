from django.contrib import admin
from shop.models import Product, Category

class ProductAdmin(admin.ModelAdmin):
    list_display = ('p_name', 'category')
    prepopulated_fields = {'slug': ('p_name',)}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('c_name',)}


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)