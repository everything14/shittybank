from django.urls import path
from .views import create_wallet, initiate_settlement, get_settlement_events

urlpatterns = [
    path('wallet/<str:id>', create_wallet, name='create_wallet'),
    path('settle/', initiate_settlement, name='initiate_settlement'),
    path('settle/<str:from_id>', get_settlement_events, name='get_settlement_events'),
]
