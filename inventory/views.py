from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status
from django.contrib.auth.models import User
from .models import Manager, InventoryItem
from rest_framework.permissions import IsAuthenticated
from .serializers import InventoryItemSerializer
from django.shortcuts import get_object_or_404
from .utils import get_logger, get_cache, set_cache, redis_client


logger = get_logger()

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        logger.debug(f"Attempting to log in user: {username}")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            logger.info(f"User {username} logged in successfully.")
            return Response({
                "username": user.username,
                "userid": user.id,
                "email": user.email,
                "phone_number": user.manager.phone_number,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        else:
            logger.warning(f"Failed login attempt for user: {username}")
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out successfully.")
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            logger.error(f"Error during logout: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")
        phone_number = request.data.get("phone")

        logger.debug(f"Attempting to register user: {username}")
        user = authenticate(username=username, password=password)
        if user:
            logger.warning(f"User {username} already exists.")
            return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            Manager.objects.create(user=user, phone_number=phone_number)
            logger.info(f"User {username} registered successfully.")
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

class InventoryItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InventoryItemSerializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            logger.info("Inventory item created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Error creating inventory item.")
        return Response({"error": "Error creating Item."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, item_id=None):
        if item_id is None:
            items = InventoryItem.objects.all()
            serializer = InventoryItemSerializer(items, many=True)
            logger.info("Retrieved all inventory items.")
            return Response(serializer.data)

        cache_key = f'inventory_item_{item_id}'
        item = get_cache(cache_key)

        if item is None:
            item = get_object_or_404(InventoryItem, id=item_id)
            serializer = InventoryItemSerializer(item)
            set_cache(cache_key, serializer.data, timeout=60 * 15)
            logger.info(f"Retrieved inventory item with ID {item_id} from database and cached it.")
            return Response(serializer.data)
        else:
            logger.info(f"Retrieved inventory item with ID {item_id} from cache.")
            return Response(item)

    def put(self, request, item_id):
        item = get_object_or_404(InventoryItem, id=item_id)
        serializer = InventoryItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            updated_item = serializer.save()
            cache_key = f'inventory_item_{item_id}'
            set_cache(cache_key, serializer.data, timeout=60 * 15)
            logger.info(f"Inventory item with ID {item_id} updated successfully.")
            return Response(serializer.data)
        logger.error(f"Error updating inventory item with ID {item_id}.")
        return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        item = get_object_or_404(InventoryItem, id=item_id)
        item.delete()
        cache_key = f'inventory_item_{item_id}'
        redis_client.delete(cache_key)  # Delete from Redis cache
        logger.info(f"Inventory item with ID {item_id} deleted successfully.")
        return Response({"message": "Item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
