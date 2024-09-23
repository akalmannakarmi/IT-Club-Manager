from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Comment(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	message = models.TextField()

class Post(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	title = models.CharField()
	details = models.TextField()
	comments = models.ManyToManyField(Comment)