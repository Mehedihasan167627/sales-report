from django.urls import path 
from .views import*



urlpatterns = [
    path("",SaleAPIView.as_view()),
    path("<int:pk>/",SaleAPIView.as_view()),
    path('report/', SalesReportAPIView.as_view()),
    
]