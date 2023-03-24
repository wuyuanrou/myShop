from django.db import models


#  migrate 命令选中所有还没有执行过的迁移（Django 通过在数据库中创建一个特殊的表 django_migrations 来跟踪执行过哪些迁移）并应用在数据库上 - 也就是将你对模型的更改同步到数据库结构上。
# 迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表
# 对应数据表，属性对应字段
# python manage.py makemigrations python manage.py migrate同步模型
class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100, default="user")
    user_password = models.CharField(max_length=100, default="123456")
    user_info = models.CharField(max_length=200, default="uhoh，还没有关于该用户的介绍呢~")


class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    artist_name = models.CharField(max_length=100, default="未知艺人")
    artist_info = models.CharField(max_length=200, default="该艺人还没有任何资料")


class Activity(models.Model):
    activity_id = models.AutoField(primary_key=True)
    activity_name = models.CharField(max_length=100, default="未知活动")
    activity_info = models.CharField(max_length=200, default="该活动还没有任何资料")
    activity_city = models.CharField(max_length=100, default="城市未定")
    activity_spot = models.CharField(max_length=200, default="场地未定")
    activity_time = models.CharField(max_length=100, default="时间未定")
    activity_price = models.IntegerField(default=0)
    activity_tickets_total = models.IntegerField(default=0)  # 票数
    activity_tickets_sold = models.IntegerField(default=0)  # 已售票数
    artist_id = models.ForeignKey('Artist', on_delete=models.CASCADE)


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    activity_id = models.ForeignKey('Activity', on_delete=models.CASCADE)
    is_sell = models.IntegerField(default=0)  # 是否已售出，未售出则为0，已售出则为user_id
    buyer_name = models.CharField(max_length=100, default="")  # 必填
    getter_name = models.CharField(max_length=100, default="")  # 必填
    phone = models.CharField(max_length=100, default="")  # 必填
    seat = models.CharField(max_length=100, default="")  # 必填 #几区几排几列


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    activity_id = models.ForeignKey('Activity', on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100, default="")
    getter_name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")
    seat = models.CharField(max_length=100, default="")  # 几区几排几列


class Like(models.Model):
    like_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    activity_id = models.ForeignKey('Activity', on_delete=models.CASCADE)

# class Goods(models.Model):
#     goods_id = models.AutoField(primary_key=True)
#     goods_name = models.CharField(max_length=100)
#     goods_price=models.FloatField()
#     goods_image = models.ImageField()
#     goods_info = models.TextField()

# class Order(models.Model):
#     order_id = models.AutoField(primary_key=True)
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     goods_id = models.ForeignKey(Goods, on_delete=models.CASCADE)
#     order_time=models.DateTimeField(auto_now=True)
