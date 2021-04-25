from django.urls import path, include

from api_v1.views import UploadDealsView, GetTopCustomers

app_name = 'api_v1'

urlpatterns = [
    path('api_v1/deals', UploadDealsView.as_view(), name='upload_deals'),
    path('api_v1/top_customers', GetTopCustomers.as_view(), name='get_top_customers'),
]
