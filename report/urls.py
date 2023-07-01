from django.urls import path
from .views import *

app_name = 'report'

urlpatterns = [

    path('', index, name='weekly_drink_report'),

]
