from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^myorders/$', views.show_my_orders, name='show_orders'),
]