from django.contrib import admin
from .models import BookInfo,PeopleInfo
# Register your models here.
class BookInfoAdmin(admin.ModelAdmin):
    list_display = ['id','name']
class PeopleInfoAdmin(admin.ModelAdmin):
    list_display = ['id','name']

admin.site.register(BookInfo,BookInfoAdmin)
admin.site.register(PeopleInfo,PeopleInfoAdmin)