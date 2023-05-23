from django.shortcuts import get_object_or_404, render
from .models import Activity, Like, Cart
from .forms import CartForm, DeleteCartForm
from django.http import HttpResponse, JsonResponse

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