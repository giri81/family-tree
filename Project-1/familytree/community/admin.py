from django.contrib import admin

# Register your models here.

from django.contrib import admin
from . import models


# Register your models here.
class CommunityMemberInline(admin.TabularInline):
    model = models.CommunityMember


admin.site.register(models.Community)
