from django.urls import path

from . import pages, user, activity, ticket, cart, like

app_name = 'myShop'
urlpatterns = [
    # 在这里剩余文本匹配了 '<int:question_id>/'，使得我们 Django 以如下形式调用 detail(request, question_id=)
    path('', pages.index, name='index'),  # name是全局唯一，用来代替html模板中对应的url
    path('about/', pages.about, name='about'),
    path('register_page/', pages.register_page, name='register_page'),
    path('login_page/', pages.login_page, name='login_page'),
    path('register/', user.register, name='register'),
    path('login_check/', user.login_check, name='login_check'),
    path('change_password/', user.change_password, name='change_password'),
    path('logout/', user.logout, name='logout'),
    path('user_page/', user.user_page, name='user_page'),
    path('activities/', activity.activities, name='activities'),
    path('<int:activity_id>/detail/', activity.activity_detail, name='activity_detail'),
    path('buy_ticket/', ticket.buy_ticket, name='buy_ticket'),
    path('delete_ticket/', ticket.delete_ticket, name='delete_ticket'),
    path('add_cart/', cart.add_cart, name='add_cart'),
    path('delete_cart/', cart.delete_cart, name='delete_cart'),
    path('add_like/', like.add_like, name='add_like'),
    path('delete_like/', like.delete_like, name='delete_like'),
]
