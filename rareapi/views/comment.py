from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Comment, RareUser, Post

class Comments(ViewSet):

    def list(self, request):
        comments = Comments.objects.all()

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        
        postId = pk
        comments = Comment.objects.filter(post_id=postId)

        serializer = CommentSerializer(
            comments, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        rareuser = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])

        comment = Comment()
        comment.rareuser =  rareuser
        comment.post = post
        comment.comment = request.data["comment"]
        comment.date = request.data["date"]

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('username',)

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    
    class Meta:
        model = RareUser

        fields = ('id', 'user')

class CommentSerializer(serializers.ModelSerializer):
    rareuser = RareUserSerializer(many=False)
    
    class Meta:
        model = Comment
       
        
        fields = ('rareuser', 'comment', 'date')
        depth = 2
