from .serializers import FcRatingSerializer,FcRatingUpdateSerializer
from .models import FcRating
from rest_framework import generics
from django.shortcuts import get_object_or_404


class FcRatingView(generics.CreateAPIView):
    serializer_class = FcRatingSerializer


class FcRatingUpdateView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FcRatingUpdateSerializer

    def get_object(self):
        rating_id = self.kwargs.get('rating_id')
        user_rating_obj = get_object_or_404(FcRating,id=rating_id)
        return user_rating_obj


class GetUserRatingView(generics.ListAPIView):
    serializer_class = FcRatingSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        ratings = FcRating.objects.filter(user=user_id)
        return ratings
