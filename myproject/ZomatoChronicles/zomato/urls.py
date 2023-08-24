from django.urls import path, re_path
from . import views

urlpatterns = [
    path('api/menu_items/', views.display_menu, name='menu_items_api'),
    path('display_orders/', views.display_orders, name='display_orders'),
    path('api/add_dish/', views.add_dish, name='add_dish_api'),
    path('api/remove_dish/<str:dish_id>/', views.remove_dish, name='remove_dish_api'),
    path('api/update/<str:dish_id>/', views.update, name='update_api'),
    path('api/take_order/', views.take_order, name='take_order_api'),
    path('api/update_status/<str:order_id>/', views.update_status, name='update_status_api'),
    path('api/chatbot/', views.chatbot, name='chatbot_api'),
]