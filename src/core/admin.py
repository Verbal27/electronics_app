from django.contrib import admin
from .models import Category, Subcategory, Payment, Order, OrderItem

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Payment)
admin.site.register(OrderItem)
admin.site.register(Order)
