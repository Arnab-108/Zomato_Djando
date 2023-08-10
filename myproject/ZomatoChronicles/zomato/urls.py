from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_menu, name='display_menu'),
    path('add' , views.add_dish , name='add_dish'),
    path('remove/<int:dish_id>/', views.remove_dish, name='remove_dish'),
    path('update/<int:dish_id>/' , views.update_availability , name='update_availability'),
    path('take_order/', views.take_order, name='take_order'),
    path('update_status/<int:order_id>/', views.update_status, name='update_status'),
    # Add more URL patterns for other views
]