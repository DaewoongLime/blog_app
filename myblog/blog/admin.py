from django.contrib import admin
from .models import Post, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer')
    list_filter = ('date','likes')
    fields = ['title', 'writer', 'content', ('date', 'likes')]

    inlines = [CommentInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'writer')
    list_filter = ('date', 'likes', 'dislikes')
    fieldsets = (
        (None, {'fields': ('post', 'writer', 'content', 'date')}),
        ('Likeness', {'fields': ('likes', 'dislikes')})
    )