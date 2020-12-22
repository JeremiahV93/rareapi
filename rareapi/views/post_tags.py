from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rareapi.models import Post, Tag, PostTag, RareUser


class PostTags(ViewSet):

    def create(self, request):

        
        
        for each in request.data:
            post = Post.objects.get(pk=each['postid'])
            tag = Tag.objects.get(pk=each['id'])

            if each['status'] == 'create':
                rareuser = RareUser.objects.get(user=request.auth.user)

                post_tag = PostTag()
                post_tag.post = post
                post_tag.tag = tag
                post_tag.save()
                
            elif each['status'] == 'delete':
                post_tag = PostTag.objects.get(tag=tag, post=post)
                post_tag.delete()

        return Response({}, status.HTTP_204_NO_CONTENT)
