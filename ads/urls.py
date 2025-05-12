from django.urls import path
from .views import ad_list_view


urlpatterns = [
    path('', ad_list_view, name='ad_list'),
]