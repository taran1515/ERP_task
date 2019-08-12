from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete='cascade')

    college_name = models.CharField(max_length=30 ,default="IIITDMJ",null=True)

