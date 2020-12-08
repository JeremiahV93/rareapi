from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE

class Post(models.Model):
    rareuser = models.ForeignKey("RareUser",  on_delete=models.CASCADE, related_name="posts", related_query_name="post")
    category = models.ForeignKey("Category",  on_delete=models.CASCADE, related_name="categories", related_query_name="category")
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=250)
    content = models.TextField(_(""))
    approved = True
