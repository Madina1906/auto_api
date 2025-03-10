from django.urls import path
from .views import login, AutoPlateListCreate, BidListCreate

urlpatterns = [
    path('login/', login, name='login'),
    path('plates/', AutoPlateListCreate.as_view(), name='plate-list'),
    path('bids/', BidListCreate.as_view(), name='bid-list'),
]
