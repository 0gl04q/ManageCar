from django.db import models
from django.contrib.auth.models import User
from manual.models import City


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.SET_NULL)
#
#
#     def __str__(self):
#         return self.user.username
# 2