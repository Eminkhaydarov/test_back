from django.db import models
from django.utils.text import slugify


# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    URL = models.CharField(max_length=255)
    named_url = models.CharField(max_length=255, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    menu_main = models.ForeignKey('Menu', on_delete=models.CASCADE, blank=False, related_name='menu')

    def __str__(self):
        return self.name


class Menu(models.Model):
    menu_name = models.CharField(max_length=255)
    URL = models.URLField(max_length=255, null=True, blank=True)
    named_url = models.CharField(max_length=255, null=True, blank=True)