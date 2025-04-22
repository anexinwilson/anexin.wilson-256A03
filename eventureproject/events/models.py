from django.db import models
from django.contrib.auth.models import User 

class Group(models.Model):
    group_name = models.CharField(max_length=100)

    def __str__(self):
        return self.group_name

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        return self.user.username  

class Events(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    users = models.ManyToManyField(Users, related_name='registered_events')

    def __str__(self):
        return self.name
