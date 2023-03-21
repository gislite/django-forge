from django.urls import path,re_path
from .views import *

# (name="upload_file_update"),
urlpatterns = [

    path("list/", UploadfileListView.as_view(), name="upload_file_list" ),
    path("download/<int:fid>/",download_file_stream, name="download_file" ),
]

