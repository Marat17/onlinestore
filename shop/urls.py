from django.urls import path, re_path
from shop import views

urlpatterns = [
	path('', views.index, name = 'index'),
	re_path(r'^product/(?P<product_name_slug>[\w\-]+)/$', views.show_product, name = 'show_product'),
	re_path(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.show_category, name = 'show_category'),
]
