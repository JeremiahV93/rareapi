from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class PostTag(models.Model):
    post = models.ForeignKey("Post",  on_delete=models.CASCADE, related_name="posttags")
    tag = models.ForeignKey("Tag",  on_delete=models.CASCADE, related_name="posttags")
