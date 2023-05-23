from django.shortcuts import get_object_or_404, render
from .models import User,Ticket, Like, Cart
from .forms import RegisterForm, LoginForm, ChangePasswordForm
from django.http import HttpResponse, JsonResponse

# 注册-成功则跳转首页
def register(request):
    form = RegisterForm(request.POST)
    if form.is_valid():
        user_name = form.cleaned_data.get('user_name')
        user_password = form.cleaned_data.get('user_password')
        user_info = form.cleaned_data.get('user_info')
        if user_info == "":
            user = User(
                user_name=user_name,
                user_password=user_password,
            )
        else:
            user = User(
                user_name=user_name,
                user_password=user_password,
                user_info=user_info
            )
        user.save()
        response = render(request, '../templates/html/index.html', {'isShow': False})
        response.set_cookie('user_id', user.user_id, max_age=300)  # 5分钟过期
        return response
    else:
        return render(request, '../templates/html/fail.html')


# 登录校验-成功则跳转首页
def login_check(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user_id = form.cleaned_data.get('user_id')
        user_password = form.cleaned_data.get('user_password')
        try:
            compare_user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return HttpResponse("清先注册")
        else:
            if user_password == compare_user.user_password:
                response = render(request, '../templates/html/index.html', {'isShow': False})
                response.set_cookie('user_id', user_id, max_age=None, expires=None, path='/',
                                    domain=None)  # 5分钟后过期
                return response
            else:
                return HttpResponse("密码或账号错误")
    else:
        # print(form.errors)
        # print(form.non_field_errors)
        return HttpResponse("资料没有填写完整或者资料填写有误")


# 注销
def logout(request):
    response = render(request, '../templates/html/success.html')
    response.delete_cookie('user_id')
    return response


# 修改密码
def change_password(request):
    form = ChangePasswordForm(request.POST)
    if form.is_valid():
        new_password = form.cleaned_data.get('new_password')
        user_id = request.COOKIES.get('user_id')
        if new_password != "":
            user = User.objects.get(user_id=user_id)
            user.user_password = new_password
            user.save()
            return render(request, '../templates/html/success.html')
    else:
        print(form.errors)
        print(form.non_field_errors)
        return render(request, '../templates/html/fail.html')

# 用户页（用户名+用户的门票）
def user_page(request):
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        user = get_object_or_404(User, user_id=user_id)
        tickets = Ticket.objects.filter(is_sell=user_id)
        like_list = Like.objects.filter(user_id=user_id)
        cart_list = Cart.objects.filter(user_id=user_id)
        user = {
            'user_id': user_id,
            'user_name': user.user_name,
            'user_info': user.user_info,
            'tickets': tickets,
            'like_list': like_list,
            'cart_list': cart_list
        }
        return render(request, '../templates/html/user_page.html',
                      {'status': 1, 'user': user, 'isShow': False})
    else:
        return render(request, '../templates/html/user_page.html', {'status': 0, 'isShow': True})
