from django.urls import path, include

from api_v1.views import UploadDealsView

app_name = 'api_v1'

urlpatterns = [
    path('api_v1/upload_deals', UploadDealsView.as_view(), name='upload_deals'),
]