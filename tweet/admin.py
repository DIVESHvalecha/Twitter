from django.contrib import admin
from .models import Tweet, Comments, profile

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1
    
class TweetAdmin(admin.ModelAdmin):
    inlines = [CommentInline]
    
admin.site.register(Tweet, TweetAdmin)
admin.site.register(profile)
