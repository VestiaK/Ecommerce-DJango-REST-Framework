from django.urls import path, include
from . import *
from rest_framework.routers import DefaultRouter
from .views import *
# from .views import ItemListViewSet, ItemDetailView
from api.views import UserRegistrationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
     # path('items/', views.item_list, name='itemlist'),
     # path('items/<int:id>', views.item_detail, name='itemdetail'),
     # path('items/', ItemListViewSet.as_view(), name='itemdetail') #2,
     # path('items/<int:id>',ItemDetailView.as_view(),name='itemdetail')#2,
     path('',include(router.urls)),
     path('token/',TokenObtainPairView.as_view()),
     path('token/refresh/',TokenRefreshView.as_view()),

     path('api/register/', UserRegistrationView.as_view(), name='register'),
     path('register/', UserRegistrationView.as_view(), name='register'),
     path('user-detail/<int:user_id>/', UserDetailView.as_view(), name="user-detail"),
     path('user-detail/', UserDetailView.as_view(), name="user-details"),
     ]
