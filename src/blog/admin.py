from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_date", "published_date"]
    list_filter = ["created_date", "published_date"]
    search_fields = ["title", "text"]
    prepopulated_fields = {"slug": ("title",)}
    class Meta:
        model = Post

admin.site.register(Post, PostAdmin)