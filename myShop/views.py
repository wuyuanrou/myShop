from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .models import User, Activity, Ticket, Like, Cart
from .forms import RegisterForm, LoginForm, ChangePasswordForm, BuyTicketForm, \
    DeleteTicketForm, LikeForm, DeleteLikeForm, CartForm, DeleteCartForm
from .tests import like_activities, raw_activities


# Create your views here.
def index(request):
    if 'user_id' in request.COOKIES:
        return render(request, '../templates/html/index.html', {'isShow': False})
    else:
        return render(request, '../templates/html/index.html', {'isShow': True})


def about(request):
    if 'user_id' in request.COOKIES:
        return render(request, '../templates/html/about.html', {'isShow': False})
    else:
        return render(request, '../templates/html/about.html', {'isShow': True})


def login_page(request):
    return render(request, '../templates/html/login.html')


def register_page(request):
    return render(request, '../templates/html/register.html')


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
        return HttpResponse("请把资料填写完整")


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


def activities(request):
    activities_data = Activity.objects.all()
    if 'user_id' in request.COOKIES:
        user_id = request.COOKIES.get('user_id')
        like_list = Like.objects.filter(user_id=user_id)
        cart_list = Cart.objects.filter(user_id=user_id)
        activities_list = like_activities(activities_data, like_list, cart_list)
        return render(request, '../templates/html/activities.html', {"activities": activities_list, 'isShow': False})
    else:
        activities_list = raw_activities(activities_data)
        return render(request, '../templates/html/activities.html',
                      {"activities": activities_list, 'isShow': True})



def activity_detail(request, activity_id):
    try:
        activity_data = Activity.objects.get(activity_id=activity_id)
    except Activity.DoesNotExist:
        return render(request, '../templates/html/fail.html')
    else:
        return render(request, '../templates/html/activity_detail.html', {'activity': activity_data, })


def buy_ticket(request):
    if 'user_id' in request.COOKIES:
        form = BuyTicketForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            activity_id = form.cleaned_data.get('activity_id')
            activity = Activity.objects.get(activity_id=activity_id)

            seat_area = form.cleaned_data.get('seat_area')  # 必填 #几区几排几列
            seat_column = form.cleaned_data.get('seat_column')
            seat_row = form.cleaned_data.get('seat_row')
            seat = seat_area + seat_column + seat_row
            same_tickets = Ticket.objects.filter(activity_id=activity_id).filter(seat=seat).count()

            if activity.activity_tickets_total == activity.activity_tickets_sold:
                return HttpResponse("票已售罄")
            elif same_tickets > 0:
                return HttpResponse("请选择其他座位")
            else:
                activity.activity_tickets_sold += 1
                activity.save()

                user_id = request.COOKIES.get('user_id')
                buyer_name = form.cleaned_data.get('buyer_name')  # 必填
                getter_name = form.cleaned_data.get('getter_name')  # 必填
                phone = form.cleaned_data.get('phone')  # 必填
                ticket = Ticket(
                    activity_id=activity,
                    is_sell=user_id,  # 是否已售出，未售出则为0，已售出则为user_id
                    buyer_name=buyer_name,
                    getter_name=getter_name,
                    phone=phone,
                    seat=seat,
                )
                ticket.save()  # 增
                # 购票成功
                return render(request, '../templates/html/success.html')
        else:
            return render(request, '../templates/html/fail.html')
    else:
        return render(request, '../templates/html/login.html')


# 退票（页面存有ticket_id， post传上来）
def delete_ticket(request):
    form = DeleteTicketForm(request.POST)
    if form.is_valid():
        try:
            ticket_id = form.cleaned_data.get('ticket_id')
            ticket = Ticket.objects.get(ticket_id=ticket_id)
        except Ticket.DoesNotExist():
            return JsonResponse({"msg": "退票-移除对象不存在", "status": 500})
        else:
            ticket.delete()
            activity = Activity.objects.get(activity_id=ticket.activity_id.activity_id)
            activity.activity_tickets_sold -= 1
            activity.save()
            return JsonResponse({"msg": "退票-成功", "status": 200})
    else:
        return JsonResponse({"msg": "退票-表单错误", "status": 412})


def add_like(request):
    if 'user_id' in request.COOKIES:
        form = LikeForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            activity_id = form.cleaned_data.get('activity_id')
            activity = Activity.objects.get(activity_id=activity_id)
            user_id = request.COOKIES.get('user_id')
            like = Like(
                user_id=user_id,
                activity_id=activity,
            )
            like.save()  # 增
            # 收藏成功
            return JsonResponse({"msg": "收藏-成功", "status": 200})
        else:
            return JsonResponse({"msg": "收藏-表单错误", "status": 412})
    else:
        return JsonResponse({"msg": "未登录", "status": 403})


def delete_like(request):
    form = DeleteLikeForm(request.POST)
    if form.is_valid():
        try:
            like_id = form.cleaned_data.get('like_id')
            user_id = request.COOKIES.get('user_id')
            like = Like.objects.get(like_id=like_id, user_id=user_id)
        except Like.DoesNotExist():
            return JsonResponse({"msg": "取消收藏-移除对象错误", "status": 500})
        else:
            like.delete()
            return JsonResponse({"msg": "取消收藏-成功", "status": 200})
    else:
        return JsonResponse({"msg": "取消收藏-表单错误", "status": 412})


def add_cart(request):
    if 'user_id' in request.COOKIES:
        form = CartForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            activity_id = form.cleaned_data.get('activity_id')
            activity = Activity.objects.get(activity_id=activity_id)
            user_id = request.COOKIES.get('user_id')
            cart = Cart(
                user_id=user_id,
                activity_id=activity,
            )
            cart.save()  # 增
            # 收藏成功
            return JsonResponse({"msg": "加入购物车-成功", "status": 200})
        else:
            return JsonResponse({"msg": "加入购物车-表单错误", "status": 412})
    else:
        return JsonResponse({"msg": "未登录", "status": 403})


def delete_cart(request):
    form = DeleteCartForm(request.POST)
    if form.is_valid():
        try:
            cart_id = form.cleaned_data.get('cart_id')
            user_id = request.COOKIES.get('user_id')
            cart = Cart.objects.get(cart_id=cart_id, user_id=user_id)
        except Like.DoesNotExist():
            return JsonResponse({"msg": "移出购物车-移除对象错误", "status": 500})
        else:
            cart.delete()
            return JsonResponse({"msg": "移出购物车-成功", "status": 200})
    else:
        return JsonResponse({"msg": "移出购物车-表单错误", "status": 412})
