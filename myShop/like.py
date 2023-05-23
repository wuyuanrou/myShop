from django.shortcuts import get_object_or_404, render
from .models import Activity, Like
from .forms import LikeForm, DeleteLikeForm
from django.http import HttpResponse, JsonResponse

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