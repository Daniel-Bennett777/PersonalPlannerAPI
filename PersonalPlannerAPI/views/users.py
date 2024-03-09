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
    user = UserSerializer()
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = PPUser
     
        fields = ('id','user','city', 'state', 'address', 'zipcode', 'profile_picture')

class PPUserViewSet(viewsets.ViewSet):
    queryset = PPUser.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PPUserSerializer
    
    def get_object(self):
        # This assumes that you are using the 'pk' parameter for lookup.
        pk = self.kwargs.get('pk')
        return PPUser.objects.get(pk=pk)


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
                user=user,
                profile_picture=request.data.get('profile_picture', None)
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
                'profile_picture': pp_user.profile_picture.url if pp_user.profile_picture else None
            }

            return Response(data, status=status.HTTP_201_CREATED)

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
        
        
        
    @action(detail=False, methods=["get"], url_path="ppusers")
    def get_pp_users(self, request):
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"error": "Authentication required"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Filter PPUser objects for the current authenticated user
        pp_users = PPUser.objects.filter(user=request.user).first()

        # Check if the PPUser exists
        if pp_users:
            serializer = PPUserSerializer(pp_users)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "PPUser not found"}, status=status.HTTP_404_NOT_FOUND
            )
            
    def list(self, request):
        pp_users = PPUser.objects.all()
        serializer = PPUserSerializer(pp_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            pp_user_instance = PPUser.objects.get(pk=pk)
            serializer = PPUserSerializer(pp_user_instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except PPUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            pp_user_instance = PPUser.objects.get(pk=pk)
        except PPUser.DoesNotExist:
            return Response({"error": "PPUser not found"}, status=status.HTTP_404_NOT_FOUND)

        user_data = request.data.pop('user', {})  # Extract user data if provided
        user_instance = pp_user_instance.user
        user_serializer = UserSerializer(user_instance, data=user_data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()

        pp_user_serializer = PPUserSerializer(pp_user_instance, data=request.data, partial=True)
        if pp_user_serializer.is_valid():
            pp_user_serializer.save()
            return Response(pp_user_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(pp_user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['patch'], url_path='add-profile-picture')
    def add_profile_picture(self, request, pk=None):
        try:
            pp_user_instance = PPUser.objects.get(pk=pk)
        except PPUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        profile_picture = request.data.get('profile_picture')

        if profile_picture:
            pp_user_instance.profile_picture = profile_picture
            pp_user_instance.save()
            serializer = PPUserSerializer(pp_user_instance)
            print("Updated PPUser:", serializer.data)  # Add this line for debugging
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Profile picture data not provided'}, status=status.HTTP_400_BAD_REQUEST) 
        
    @action(detail=True, methods=["get"], url_path="profile-picture")
    def get_profile_picture(self, request, pk=None):
        try:
            pp_user_instance = PPUser.objects.get(pk=pk)
        except PPUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        profile_picture_url = pp_user_instance.profile_picture.url if pp_user_instance.profile_picture else None
        return Response({"profile_picture": profile_picture_url}, status=status.HTTP_200_OK)