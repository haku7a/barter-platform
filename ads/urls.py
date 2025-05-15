from django.urls import path
from .views import (ad_list_view, 
                    ad_create_view, 
                    ad_update_view, 
                    ad_delete_view, 
                    exchange_proposal_create_view,
                    exchange_proposal_list_view,
                    update_exchange_proposal_status_view,)

app_name = 'ads'

urlpatterns = [
    path('', ad_list_view, name='ad_list'),
    path('create/', ad_create_view, name='ad_create'),
    path('ad/<int:pk>/edit/', ad_update_view, name='ad_update'),
    path('ad/<int:pk>/delete/', ad_delete_view, name='ad_delete'),
    path('ad/<int:ad_receiver_pk>/propose/', exchange_proposal_create_view, name='exchange_proposal_create'),
    path('proposals/', exchange_proposal_list_view, name='exchange_proposal_list'),
    path('proposals/<int:proposal_pk>/status/<str:new_status>/', update_exchange_proposal_status_view, name='exchange_proposal_update_status'),
]