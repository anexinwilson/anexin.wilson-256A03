from django.db import models
from django.contrib.auth.models import User 

# Table to store user types
class Group(models.Model):
    group_name = models.CharField(max_length=100)

    def __str__(self):
        # Show the event group name when printed
        return self.group_name


# Table to extend Django's built-in User and link it with a group
class Users(models.Model):
    # Link to Django's User table, and if a user is deleted, delete this entry too
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    # Link to the Group table, delete this if the group is deleted
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        # Show the event username when printed
        return self.user.username  


# Table to store event details
class Events(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    # Links multiple users to a event
    users = models.ManyToManyField(Users, related_name='registered_events')

    def __str__(self):
        # Show the event name when printed
        return self.name
