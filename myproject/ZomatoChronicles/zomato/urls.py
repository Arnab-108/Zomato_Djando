from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.display_menu, name='display_menu'),
    path('add' , views.add_dish , name='add_dish'),
    re_path(r'^remove/(?P<dish_id>[a-f0-9]{24})/$', views.remove_dish, name='remove_dish'),
    path('update/<str:dish_id>/', views.update, name='update'),
    path('take_order/', views.take_order, name='take_order'),
    path('update_status/<str:order_id>/', views.update_status, name='update_status'),
    # Add more URL patterns for other views
]