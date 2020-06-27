from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):

    title = models.CharField(max_length=500)

    content = models.TextField()

    date_posted = models.DateTimeField(default=timezone.now)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #Return the title of the object/s
    def __str__(self):
        if self.title:
            return self.title
        else:
            return self.author

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
