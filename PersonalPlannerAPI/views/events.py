from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from PersonalPlannerAPI.models import Category, Event, PPUser
from .users import PPUserSerializer
from .category import CategorySerializer
from rest_framework import permissions
from rest_framework.permissions import AllowAny 

class EventSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=PPUser.objects.all())
    is_owner = serializers.SerializerMethodField()
    category = CategorySerializer(many=False)
    attendees = PPUserSerializer(many=True, read_only=True)

    def get_is_owner(self, obj):
        return self.context["request"].user == obj.user.user

    class Meta:
        model = Event
        fields = [
            "id",
            "user",
            "category",
            "title",
            "description",
            "date_posted",
            "event_date",  # Changed from "date"
            "event_time",  # New field for time
            "city",
            "state",
            "address",
            "zipcode",
            "is_owner",
            "attendees" 
        ]

        extra_kwargs = {"description": {"required": False}, "date_posted": {"read_only": True}}

class EventViewSet(viewsets.ViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [AllowAny]

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
        event_date = request.data.get("event_date")  # Changed from "date"
        event_time = request.data.get("event_time")  # New field for time
        description = request.data.get("description")
        city = request.data.get("city")
        address = request.data.get("address")
        state = request.data.get("state")
        zipcode = request.data.get("zipcode")

        event = Event.objects.create(
            user=user,
            title=title,
            event_date=event_date,
            event_time=event_time,
            description=description,
            category=category,
            city=city,
            state=state,
            address=address,
            zipcode=zipcode,
        )

        serializer = EventSerializer(event, context={"request": request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None, *args, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update the fields as needed
        event.title = request.data.get("title", event.title)
        event.event_date = request.data.get("event_date", event.event_date)  # Changed from "date"
        event.event_time = request.data.get("event_time", event.event_time)  # New field for time
        event.description = request.data.get("description", event.description)
        event.city = request.data.get("city", event.city)
        event.address = request.data.get("address", event.address)
        event.state = request.data.get("state", event.state)
        event.zipcode = request.data.get("zipcode", event.zipcode)

        category_id = request.data.get("category")
        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
                event.category = category
            except Category.DoesNotExist:
                return Response({"detail": "Category not found"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the updated event
        event.save()

        serializer = EventSerializer(event, context={"request": request})
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response({"detail": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        # Delete the event
        event.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
    @action(detail=True, methods=['patch'])
    def rsvp(self, request, pk=None):
        try:
            event = Event.objects.get(pk=pk)
            user = request.user.pp_user

            # Check if the user has already RSVP'd
            if user in event.attendees.all():
                return Response({"detail": "User has already RSVP'd to this event"}, status=status.HTTP_400_BAD_REQUEST)

            # Add user to attendees with ppuser.id
            attendee_data = {
                'id': user.id,  # assuming user.id is the ppuser.id
                'city': user.city,
                'state': user.state,
                'address': user.address,
                'zipcode': user.zipcode,
            }

            event.attendees.add(user)
            event.save()

            # Fetch updated event details with attendees data
            updated_event = Event.objects.get(pk=pk)
            serializer = EventSerializer(updated_event, context={"request": request})
            return Response(serializer.data)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)