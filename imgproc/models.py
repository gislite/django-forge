from django.db import models

# Create your models here.


# models.py
from django.db import models
from django.urls import reverse


# Create your models here.
class UploadFile(models.Model):
    title = models.CharField(max_length=30)
    uploadfile = models.ImageField(upload_to="upload/")

    def __str__(self) -> str:
        return self.title
