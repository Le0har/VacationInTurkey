from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Photo(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, related_name='photos')

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='author_comment')
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
