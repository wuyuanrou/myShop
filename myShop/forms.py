from django import forms


class RegisterForm(forms.Form):
    user_name = forms.CharField(max_length=100)
    user_password = forms.CharField(max_length=100)
    user_info = forms.CharField(max_length=200, required=False)


class LoginForm(forms.Form):
    user_id = forms.IntegerField()
    user_password = forms.CharField(max_length=100)


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(max_length=100)


class BuyTicketForm(forms.Form):
    activity_id = forms.IntegerField()
    # is_sell = forms.IntegerField()  # 是否已售出，未售出则为0，已售出则为user_id，不需要用户填写
    buyer_name = forms.CharField(max_length=100)  # 必填
    getter_name = forms.CharField(max_length=100)  # 必填
    phone = forms.CharField(max_length=100)  # 必填
    seat_area = forms.CharField(max_length=100)  # 必填 #几区几排几列
    seat_column = forms.CharField(max_length=100)
    seat_row = forms.CharField(max_length=100)


class DeleteTicketForm(forms.Form):
    ticket_id = forms.IntegerField()


class LikeForm(forms.Form):
    activity_id = forms.IntegerField()


class DeleteLikeForm(forms.Form):
    like_id = forms.IntegerField()


class CartForm(forms.Form):
    activity_id = forms.IntegerField()
    buyer_name = forms.CharField(max_length=100, required=False)
    getter_name = forms.CharField(max_length=100, required=False)
    phone = forms.CharField(max_length=100, required=False)
    seat_area = forms.CharField(max_length=100, required=False)  # 几区几排几列
    seat_column = forms.CharField(max_length=100, required=False)
    seat_row = forms.CharField(max_length=100, required=False)


class DeleteCartForm(forms.Form):
    cart_id = forms.IntegerField()
