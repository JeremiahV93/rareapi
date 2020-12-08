from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class RareUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    bio = models.CharField(max_length=50)
    profile_image_url = models.CharField(max_length=250)
    created_on = models.DateField()
    active = True
