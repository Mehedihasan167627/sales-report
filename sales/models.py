from django.db import models

class Sale(models.Model):
    order_id =models.CharField(max_length=255)
    order_date=models.DateField(auto_now_add=True)
    ship_date =models.DateField()
    ship_mode =models.CharField(max_length=255)
    customer_id=models.CharField(max_length=255)
    customer_name =models.CharField(max_length=255)
    segment =models.CharField(max_length=255)
    country =models.CharField(max_length=255)
    city =models.CharField(max_length=255)
    state =models.CharField(max_length=255)
    postal_code =models.CharField(max_length=255)
    region =models.CharField(max_length=255)
    product_id =models.CharField(max_length=255)
    category =models.CharField(max_length=255)
    sub_category =models.CharField(max_length=255)
    product_name =models.CharField(max_length=255)
    sales =models.DecimalField(max_digits=10,decimal_places=2) 


    def __str__(self) -> str:
        return str(self.order_id)
    

    class Meta:
        db_table="sales_data" 

