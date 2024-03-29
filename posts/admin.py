from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "pub_date", "author", "group")
    search_fields = ("text",)
    list_filter = ("pub_date", "group",)
    empty_value_display = "-пусто-"


class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "description")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "text", "created",)
    search_fields = ("post",)
    list_filter = ("author", "created",)


class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user",)
    list_filter = ("author", "user",)


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
