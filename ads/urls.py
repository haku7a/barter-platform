from django.urls import path
from .views import ad_list_view, ad_create_view

app_name = 'ads'

urlpatterns = [
    path('', ad_list_view, name='ad_list'),
    path('create/', ad_create_view, name='ad_create'),
]