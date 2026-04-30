from django.contrib import admin
from .models import Order
from .models import OrderTag

admin.site.register(Order)
admin.site.register(OrderTag)