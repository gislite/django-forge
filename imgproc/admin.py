from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *
# Register your models here.

class UploadFileAdmin(admin.ModelAdmin):
    list_display = ['id','title','uploadfile']

admin.site.register(UploadFile,UploadFileAdmin)
