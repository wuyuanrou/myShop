from django.contrib import admin
from .models import User, Artist, Activity, Ticket, Like, Cart

admin.site.register(User)
admin.site.register(Artist)
admin.site.register(Activity)
admin.site.register(Ticket)
admin.site.register(Like)
admin.site.register(Cart)
