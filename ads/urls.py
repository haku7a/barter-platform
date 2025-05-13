from django.urls import path
from .views import ad_list_view, ad_create_view, ad_update_view, ad_delete_view

app_name = 'ads'

urlpatterns = [
    path('', ad_list_view, name='ad_list'),
    path('create/', ad_create_view, name='ad_create'),
    path('ad/<int:pk>/edit/', ad_update_view, name='ad_update'),
    path('ad/<int:pk>/delete/', ad_delete_view, name='ad_delete'),
]