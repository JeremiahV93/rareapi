from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser, Category

class Posts(ViewSet):

    def list(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()

            return Response({}, status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def create(self, request):

        rare_user = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.rare_user = rare_user

        category =  Category.objects.get(pk= request.data["categoryId"])
        post.category = category

        try:
            post.save()
            serializers =  PostSerializer(post, context={'request': request})
            return Response(serializer.data) 
        except ValidationError as ex:
            return Response({ "reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        url = serializers.HyperlinkedIdentityField(
            view_name='post',
            lookup_field='id'
        )
        fields = ('id', 'title', 'publication_date', 'image_url', 'content', 'approved')
        depth = 1
