from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers



class RareUser(ViewSet):

    def list(self, request):
        users = RareUser.objects.all()

        serializer = UserSerializer(
            users, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            users = RareUser.objects.get(pk=pk)
            

            serializer = UserSerializer(users, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        
        
        fields = ('user', 'bio', 'profile_image_url', 'created_on', 'active', 'approved')
      


