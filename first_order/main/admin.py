from django.contrib import admin
from .models import *
from .forms import *


class CustomUserAdmin(admin.ModelAdmin):
    #add_form = CustomUserCreationForm
    #form = CustomUserChangeForm
    model = CustomUser
    list_display = ['id', 'slug', 'username', 'level', 'status', 'email', 'avatar', 'password']
    prepopulated_fields = {'slug': ('username',)}


class HistoryAdmin(admin.ModelAdmin):
    model = History
    list_display = ['id', 'title', 'level', 'created_add', 'category', 'author']


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'slug', 'title']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Album)
