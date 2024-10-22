from .views import home,menu,Reservationcreateview,meal_plan,scrap,blog_detail,remove_from_cart,clear_cart
from django.urls import path
from . import views

urlpatterns=[
    path('',home,name='main'),
    path('menu/',menu,name="menu"),
    path('reservation/',Reservationcreateview.as_view(),name="reservation"),    
  path('menu1/', views.menu_view, name='menu1'),
     path('meal-plan/', meal_plan, name='meal_plan'),
     path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('user_orders/', views.user_orders, name='user_orders'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
     path('blog/', scrap, name='blog'),
     path('blogdetail/<path:link>/', blog_detail, name='blog_detail'),
      path('remove-from-cart/<str:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', clear_cart, name='clear_cart'),
    
]