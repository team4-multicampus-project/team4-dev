from django.contrib import admin
from .models import Post

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'content', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('subject', 'content')
    date_hierarchy = 'created_at'