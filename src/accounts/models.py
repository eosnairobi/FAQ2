
from django.db import models
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import uuid
from django.utils import timezone

# Holds the User account(s)


# Custom User Model
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    joined = models.DateTimeField(default=timezone.now, blank=True)
    se_account_id = models.PositiveIntegerField(null=True)
    se_user_id = models.PositiveIntegerField(null=True)
    se_reputation = models.PositiveIntegerField(null=True)
    se_link = models.URLField(null=True)
    bronze_badges = models.PositiveIntegerField(default=0)
    silver_badges = models.PositiveIntegerField(default=0)
    gold_badges = models.PositiveIntegerField(default=0)
    se_profile_image = models.URLField(null=True)
    se_display_name = models.CharField(max_length=1000)


class BlockProducer(models.Model):
    account_name = models.CharField(max_length=12, unique=True)
    producer_key = models.CharField(max_length=60)
    display_name = models.CharField(max_length=300, blank=True)
    url = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    longitude = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)
    geom = models.PointField(srid=4326, blank=True, null=True)
    public_endpoint = models.URLField(blank=True, null=True)
    # location = models.MultiPointField(srid=4326, blank=True, null=True)
    country = models.CharField(max_length=30, blank=True)
    objects = GeoManager()
    # geom = models.MultiPolygonField(srid=4326)

    # def get_location(self):
    #     return self.latitude, self.longitude

    # def get_gis_coords(self):
    #     return self.lat, self.long

    def __str__(self):
        return self.account_name


class BlockProducerData(models.Model):
    block_producer = models.ForeignKey(
        'BlockProducer', related_name='bp_position', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    position = models.PositiveIntegerField()
    unweighted_votes = models.DecimalField(
        max_digits=1000, decimal_places=18, default=0)
    weighted = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '{} - {}'.format(self.block_producer.account_name, self.timestamp)


class Node(models.Model):
    block_producer = models.ForeignKey(
        BlockProducer, on_delete=models.CASCADE, related_name='nodes')
    node_type = models.CharField(max_length=20, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    p2p_endpoint = models.URLField(null=True)
    ssl_endpoint = models.URLField(null=True)


class Country(models.Model):
    fips = models.CharField(max_length=2)
    iso2 = models.CharField(max_length=2)
    iso3 = models.CharField(max_length=3)
    un = models.IntegerField()
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.BigIntegerField()
    region = models.IntegerField()
    subregion = models.IntegerField()
    lon = models.FloatField()
    lat = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)

    def __str__(self):
        return self.name
