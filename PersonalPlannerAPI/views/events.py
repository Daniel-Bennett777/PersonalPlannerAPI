from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
# from django.contrib.auth.models import User
from PersonalPlannerAPI.models import Category, Event, PPUser
from .users import PPUserSerializer
from .category import CategorySerializer
from rest_framework import permissions

# class SimplePostSerializer(serializers.ModelSerializer):

    
#     class Meta:
#         model = Event
#         fields = [
#             "title",
#             "description",
#             "date",
#             "category",
#             "start_datetime",
#             "city",
#             "state",
#             "address",
#             "zipcode"
#         ],



class EventSerializer(serializers.ModelSerializer):
    user = PPUserSerializer(many=False)
    is_owner = serializers.SerializerMethodField()
    category = CategorySerializer(many=False)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user.user

    class Meta:
        model = Event
        fields = [
            "id",
            "user",
            "title",
            "description",
            "date",
            "category",
            "start_datetime",
            "city",
            "state",
            "address",
            "zipcode", 
            "is_owner"
        ]

        extra_kwargs = {"description": {"required": False}}
        
class EventViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True, context={"request": request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            serializer = EventSerializer(event, context={"request": request})
            return Response(serializer.data)

        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        user = PPUser.objects.get(user=request.auth.user)
        category_id = request.data.get("category")
        category = Category.objects.get(pk=category_id)
        title = request.data.get("title")
        start_datetime = request.data.get("start_datetime")
        description = request.data.get("description")
        date = request.data.get("date")
        city = request.data.get("city")
        address = request.data.get("address")
        state = request.data.get("state")
        zipcode = request.data.get("zipcode")

        event = Event.objects.create(
            user=user,
            title=title,
            start_datetime=start_datetime,
            description=description,
            date=date,
            category=category,
            city=city,
            state=state,
            address=address,
            zipcode=zipcode,
        )

        serializer = EventSerializer(event, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)