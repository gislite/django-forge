from django.urls import path,re_path
from .views import *

# (name="upload_file_update"),
urlpatterns = [

    path('foo/', index, name='index'),
]

