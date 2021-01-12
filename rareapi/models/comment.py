from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Comment(models.Model):
    rareuser = models.ForeignKey("RareUser",  on_delete=models.CASCADE, related_name="comments", related_query_name="comments")
    post = models.ForeignKey("Post",  on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    date = models.DateField()
