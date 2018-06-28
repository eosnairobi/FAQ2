
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

# Holds the User account(s)


# Custom User Model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    joined = models.DateTimeField(default=timezone.now)
    se_account_id = models.PositiveIntegerField(null=True)
    se_user_id = models.PositiveIntegerField(null=True)
    se_reputation = models.PositiveIntegerField(null=True)
    se_link = models.URLField(null=True)
    bronze_badges = models.PositiveIntegerField(default=0)
    silver_badges = models.PositiveIntegerField(default=0)
    gold_badges = models.PositiveIntegerField(default=0)
    se_profile_image = models.URLField(null=True)
    se_display_name = models.CharField(max_length=1000)


class BlockProducer(User):
    account_name = models.CharField(max_length=12)
    producer_key = models.CharField(max_length=60)
    display_name = models.CharField(max_length=300, blank=True)
    url = models.URLField()
    latitude = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    longitude = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    def get_location(self):
        return self.latitude, self.longitude

    def __str__(self):
        return self.account_name
