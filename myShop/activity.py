from django.shortcuts import get_object_or_404, render
from .models import Activity, Like, Cart
from .tests import like_activities, raw_activities
from django.http import HttpResponse, JsonResponse

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
        if 'user_id' in request.COOKIES:
            return render(request, '../templates/html/activity_detail.html', {'activity': activity_data, 'isShow': False})
        else:
            return HttpResponse('请先登陆')