from django.contrib import admin
from .models import Sale 


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display=["id","order_id",
        "region",
        "category",
        "sub_category",
        "sales"]