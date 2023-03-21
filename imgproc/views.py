from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
# Create your views here.
# from imgproc.forms import *
from .models import *
from django.views import generic
from django.urls import reverse_lazy
import os


class UploadfileListView(generic.ListView):
    """list all data """
    model = UploadFile
    template_name = "imgproc/uploadfile_list.html"


def download_file_stream(request, fid=1):
    """ Send file with FileResponse """
    obj = UploadFile.objects.get(pk=fid)
    fpath = './update'
    print(fpath)
    response = FileResponse(open(fpath, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response["Content-Disposition"] = "attachment; filename=test.jpg"
    return response
