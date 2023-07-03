from django.urls import path
from .views import frige_list, frige_state, handle_quantity

app_name = 'frige'

urlpatterns = [
    path('', frige_list, name='frige_list'),
    path('<int:frige_id>/', frige_state, name='frige_state'),
    path('quantity/', handle_quantity, name='handle_quantity'),
    path('delete/', frige_list, name='frige_delete'),
]