from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Skill(models.Model):
	name = models.CharField(max_length=100)

class Course(models.Model):
	name = models.CharField(max_length=100)

class Batch(models.Model):
	name = models.CharField(max_length=50)

class Profile(models.Model):
	userId = models.ForeignKey(User,on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	courseId = models.ForeignKey(Course,on_delete=models.DO_NOTHING)
	batchId = models.ForeignKey(Batch,on_delete=models.DO_NOTHING)
	skills = models.ManyToManyField(Skill,related_name="profiles")