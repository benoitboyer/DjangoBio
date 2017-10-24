from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
    	return "User : "+self.user.username

    def email(self):
    	return self.user.email
    def name(self):
    	return self.user.username