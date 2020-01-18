from django.db import models
from django.contrib.auth import get_user_model
from customers.models import FcServiceRequest
from django.core.validators import MinValueValidator,MaxValueValidator

User = get_user_model()


class FcRating(models.Model):
    user = models.ForeignKey(User, related_name='my_created_rating', on_delete=models.DO_NOTHING)
    rating_score = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)], null=True, blank=True)
    service_request = models.ForeignKey(FcServiceRequest, related_name='request_ratings', on_delete=models.DO_NOTHING)
    review = models.TextField('Review', max_length=200, null=True, blank=True)
    date_rated = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
