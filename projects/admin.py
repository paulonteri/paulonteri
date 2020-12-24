from django.contrib import admin
from .models import Category, SubCategory, Project, Article

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Project)
admin.site.register(Article)
