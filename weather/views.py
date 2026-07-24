from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, UserSerializer, WeatherRecordSerializer
from .models import WeatherRecord

@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Return a flat response to match the Android app's structure
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    # Get input (Android sends the email/username in both fields)
    login_input = request.data.get('email') or request.data.get('username')
    password = request.data.get('password')

    if not login_input or not password:
        return Response({'error': 'Credentials required'}, status=status.HTTP_400_BAD_REQUEST)

    # 1. Try to find the user by email first
    try:
        user_obj = User.objects.get(email=login_input)
        username = user_obj.username
    except User.DoesNotExist:
        # 2. If no user has that email, assume the input IS the username
        username = login_input

    # 3. Authenticate with the actual username and password
    user = authenticate(username=username, password=password)

    if user:
        # IMPORTANT: Return a FLAT object (id, username, email) 
        # so it matches the UserResponse class in your Android code
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid email/username or password'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'POST'])
def history_view(request):
    if request.method == 'GET':
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        records = WeatherRecord.objects.filter(user_id=user_id).order_by('-id')
        serializer = WeatherRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # The user ID is sent inside the 'user' field in the JSON
        serializer = WeatherRecordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)