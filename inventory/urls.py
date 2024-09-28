
from django.urls import path
from . views import UserLoginView, UserRegisterView, InventoryItemAPIView, UserLogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('items/', InventoryItemAPIView.as_view(), name='items'),
    path('items/<int:item_id>/', InventoryItemAPIView.as_view(), name='items'),  
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
