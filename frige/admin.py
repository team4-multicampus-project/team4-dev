from django.contrib import admin
from .models import Frige, Drink

# Register your models here.
@admin.register(Frige)
class FrigeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('name', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(Drink)
class DrinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'frige', 'quantity')
    list_filter = ('user', 'frige')
    search_fields = ('name', 'user__username', 'frige__name')
