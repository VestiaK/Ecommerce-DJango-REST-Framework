from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .models import *
from .serializers import *
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
    
# ViewSet untuk Product
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    

# ViewSet untuk Cart
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    # Menampilkan keranjang belanja pengguna
    def list(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    # Menambah item ke keranjang
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        product = Product.objects.get(id=request.data.get('product_id'))
        quantity = request.data.get('quantity', 1)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()
        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    # Menghapus item dari keranjang
    @action(detail=True, methods=['delete'])
    def remove_from_cart(self, request, pk=None):
        product = Product.objects.get(id=request.data.get('product_id'))
        cart = Cart.objects.get(user=request.user)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ViewSet untuk Order
class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # Membuat order baru dari cart
    @action(detail=False, methods=['post'])
    def create_order(self, request):
        cart = Cart.objects.get(user=request.user)
        if not cart.items.exists():
            return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(user=request.user, status="Pending")


        # Menambahkan items ke order
        for cart_item in cart.items.all():
            order_item = OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        


        # Kosongkan cart setelah order dibuat
        cart.items.all().delete()

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
