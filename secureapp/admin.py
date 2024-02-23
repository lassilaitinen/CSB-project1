from django.contrib import admin

# Register your models here.
from .models import Notice, Comment, Choice

admin.site.register(Notice)
admin.site.register(Comment)
admin.site.register(Choice)