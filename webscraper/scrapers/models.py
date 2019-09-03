from django.db import models

# Create your models here.
from django.db import models
from datetime import date



class PageUrl(models.Model):
    url = models.URLField(max_length=200, unique=True)
    creationdate = models.DateTimeField(auto_now_add=True)
    imgtask_id = models.CharField(max_length=200)


class Image(models.Model):
    url = models.ForeignKey(PageUrl, on_delete=models.CASCADE, related_name='images')
    creationdate = models.DateTimeField(auto_now_add=True)
    imageurl = models.URLField()
    # image = models.ImageField(upload_to='images')


class Text(models.Model):
    url = models.ForeignKey(PageUrl, on_delete=models.CASCADE, related_name='texts')
    creationdate = models.DateTimeField(auto_now_add=True)
    filename = models.CharField(max_length=200, unique=True)

    def save(self, *args, **kwargs):
        self.filename = f'{self.url.id}.txt'  # {self.creationdate.strftime("%d-%m-%y %H:%M:%S")}.txt'
        super().save(*args, **kwargs)

