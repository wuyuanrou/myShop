from django.urls import path

from . import views

app_name = 'myShop'
urlpatterns = [
    # 在这里剩余文本匹配了 '<int:question_id>/'，使得我们 Django 以如下形式调用 detail(request, question_id=)
    path('', views.index, name='index'),  # name是全局唯一，用来代替html模板中对应的url
    path('about/', views.about, name='about'),
    path('register_page/', views.register_page, name='register_page'),
    path('login_page/', views.login_page, name='login_page'),
    path('register/', views.register, name='register'),
    path('login_check/', views.login_check, name='login_check'),
    path('change_password/', views.change_password, name='change_password'),
    path('logout/', views.logout, name='logout'),
    path('user_page/', views.user_page, name='user_page'),
    path('activities/', views.activities, name='activities'),
    path('<int:activity_id>/detail/', views.activity_detail, name='activity_detail'),
    path('buy_ticket/', views.buy_ticket, name='buy_ticket'),
    path('delete_ticket/', views.delete_ticket, name='delete_ticket'),
    path('add_cart/', views.add_cart, name='add_cart'),
    path('delete_cart/', views.delete_cart, name='delete_cart'),
    path('add_like/', views.add_like, name='add_like'),
    path('delete_like/', views.delete_like, name='delete_like'),
]
