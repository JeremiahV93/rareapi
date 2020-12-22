from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rareapi.models import Post, RareUser, Category, PostTag, Tag
from rareapi.views.category import CategorySerializer
from rareapi.views.tag import TagSerializer
class Posts(ViewSet):

    def list(self, request):
        posts = Post.objects.all()

        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            

            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

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

        rareuser = RareUser.objects.get(user=request.auth.user)

        post = Post()
        post.title = request.data["title"]
        post.publication_date = request.data["publication_date"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.rareuser = rareuser

        category =  Category.objects.get(pk= request.data["categoryId"])
        post.category = category

        tags = request.data['posttags']

        try:
            post.save()

            for tag_id in tags:
                tag = Tag.objects.get(pk = tag_id)
                posttag = PostTag()
                posttag.post = post
                posttag.tag = tag
                posttag.save()

            serializer =  PostSerializer(post, context={'request': request})
            return Response(serializer.data) 
        except ValidationError as ex:
            return Response({ "reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        rareuser = RareUser.objects.get(user=request.auth.user)

        post = Post.objects.get(pk=pk)


        post.publication_date = request.data["publication_date"]
        post.title = request.data["title"]
        post.image_url = request.data["image_url"]
        post.content = request.data["content"]
        post.approved = request.data["approved"]
        post.rareuser = rareuser

        category =  Category.objects.get(pk= request.data["categoryId"])
        post.category = category

        post.save()

        return Response({}, status=status.HTTP_201_CREATED)

class PostTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(many=False)

    class Meta:
        model = PostTag
        fields = ['tag']

class PostSerializer(serializers.ModelSerializer):

    category = CategorySerializer(many=False)
    posttags = PostTagSerializer(many=True)
    class Meta:
        model = Post
        
        
        fields = ('id', 'title', 'publication_date', 'image_url', 'content', 'approved', 'category', 'posttags')
        depth = 1
