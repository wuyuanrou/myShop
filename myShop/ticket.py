from django.shortcuts import get_object_or_404, render
from .models import Activity, Ticket
from .forms import BuyTicketForm, \
    DeleteTicketForm
from django.http import HttpResponse, JsonResponse

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