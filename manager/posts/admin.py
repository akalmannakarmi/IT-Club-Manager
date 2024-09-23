from django.contrib import admin
from .models import Post,Comment
from .forms import PostForm,CommentForm

# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('userId', 'title', 'details')
    list_filter = ('userId',)
    search_fields = ('userId__username', 'title')
    filter_horizontal = ('comments',)



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('userId', 'message')
    list_filter = ('userId',)
    search_fields = ('userId__username')