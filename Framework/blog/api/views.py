from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Item
from .serializers import ItemSerializer
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer 



class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get (self,request):
        user = request.user
        groups = [group.name for group in user.groups.all()]
        return Response ({
            "id": user.id,
            "username" : user.username,
            "email" : user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_superuser":user.is_superuser,
            "groups":groups  
        })
        
    def put(self, request):    
            user = request.user
            user.username = request.data.get('username', user.username)  
            user.email = request.data.get('email', user.email)  
            user.first_name = request.data.get('first_name', user.first_name)  
            user.last_name = request.data.get('last_name', user.last_name)  
            user.save()
              
            return Response({"message": "Profile updated successfully!"}, status=status.HTTP_200_OK) 


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]  

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]