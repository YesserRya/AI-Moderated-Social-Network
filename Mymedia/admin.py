from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import *


class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username"]
    inlines = [ProfileInline]

class UnapprovedPost(Post):
    class Meta:
        proxy=True

class UnapprovedPostAdmin(admin.ModelAdmin):
    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(approved=False)

admin.site.register(UnapprovedPost, UnapprovedPostAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Post)

