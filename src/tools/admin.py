from django.contrib import admin

from .models import Category, Tool, SuggestedTool

admin.site.register(Category)
admin.site.register(Tool)
admin.site.register(SuggestedTool)
