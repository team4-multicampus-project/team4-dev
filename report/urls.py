from django.urls import path
from .views import *
import core.settings as settings
from django.conf.urls.static import static

app_name = 'report'

urlpatterns = [

    path('', index, name='weekly_drink_report'),

] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)