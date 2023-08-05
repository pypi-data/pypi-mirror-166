from django.urls import path
from .views import RecontactView

urlpatterns = [
    path('', RecontactView.as_view(), name='recontact_base'),
    path('sent/', RecontactView.as_view(), name='recontact_sent'),

]
