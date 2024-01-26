from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from PersonalPlannerAPI.models import PPUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "first_name", "last_name", "email"]
        extra_kwargs = {"password": {"write_only": True}}

class PPUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PPUser
        fields = ( 'city', 'state', 'address', 'zipcode')

class PPUserViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], url_path='register')
    def register_account(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user = User.objects.create_user(
                username=user_serializer.validated_data['username'],
                first_name=user_serializer.validated_data.get('first_name', ''),
                last_name=user_serializer.validated_data.get('last_name', ''),
                email=user_serializer.validated_data.get('email', ''),
                password=user_serializer.validated_data['password']
            )
            
            pp_user = PPUser.objects.create(
                city=request.data.get('city', ''),
                state=request.data.get('state', ''),
                address=request.data.get('address', ''),
                zipcode=request.data.get('zipcode', ''),
                user=user
            )
            token, created = Token.objects.get_or_create(user=user)

            data = {
                'valid': True,
                'token': token.key,
                'id': token.user.id,
                'first_name': token.user.first_name,
                'last_name': token.user.last_name,
                'username': token.user.username,
                'email': token.user.email,
                'city': pp_user.city,
                'state': pp_user.state,
                'address': pp_user.address,
                'zipcode': pp_user.zipcode,
            }

            pp_user_serializer = PPUserSerializer(data=request.data, context={"request": request})
            if pp_user_serializer.is_valid():
                return Response(data, status=status.HTTP_201_CREATED)

            user.delete()
            return Response({'error': 'Failed to serialize PPUser'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        username = request.data['username']
        password = request.data['password']

        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

        # Access the associated PPUser instance for the authenticated user
            try:
                pp_user = PPUser.objects.get(user=authenticated_user)
                pp_user_data = {
                    'city': pp_user.city,
                    'state': pp_user.state,
                    'address': pp_user.address,
                    'zipcode': pp_user.zipcode,
                }
            except PPUser.DoesNotExist:
                pp_user_data = {}

            data = {
                'valid': True,
                'token': token.key,
                'id': token.user.id,
                'first_name': token.user.first_name,
                'last_name': token.user.last_name,
                'username': token.user.username,
                'email': token.user.email,
                'pp_user': pp_user_data,
            }

            return Response(data)
        else:
            data = {'valid': False, 'error': 'Invalid username or password'}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
