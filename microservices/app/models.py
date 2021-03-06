from django.db import models

# Create your models here.

class SiteUser(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    address = models.CharField(max_length=200, null=True)
    buyer_rating = models.FloatField()
    buyer_activity_score = models.FloatField()
    seller_rating = models.FloatField()
    seller_activity_score = models.FloatField()

class Authenticator(models.Model):
    user = models.ForeignKey(SiteUser)
    authenticator = models.CharField(primary_key=True, max_length=64)
    date_created = models.DateTimeField(auto_now_add=True)

class Book(models.Model):
    title = models.CharField(max_length=300)
    ISBN = models.CharField(max_length=50)
    author = models.CharField(max_length=100)
    price = models.FloatField()
    year = models.CharField(max_length=10)
    class_id = models.CharField(max_length=15)
    edition = models.IntegerField()

    AVAILABLE = "AV"
    IN_TRANSIT = "IT"
    DELIVERED = "DE"
    STATUS_CHOICES = (
        (AVAILABLE, "Available"),
        (IN_TRANSIT, "In Transit"),
        (DELIVERED, "Delivered"),
    )
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )

    HARDCOVER = "HC"
    PAPERBACK = "PB"
    LOOSE_LEAF = "LL"
    TYPE_CHOICES = (
        (HARDCOVER, "Hardcover"),
        (PAPERBACK, "Paperback"),
        (LOOSE_LEAF, "Loose leaf"),
    )
    type_name = models.CharField(
        max_length=2,
        choices=TYPE_CHOICES,
        default=HARDCOVER
    )

    NEW = "NW"
    USED_GOOD = "UG"
    USED_BAD = "UB"
    CONDITION_CHOICES = (
        (NEW, "New"),
        (USED_GOOD, "Used, in good condition"),
        (USED_BAD, "Used, in poor condition"),
    )
    condition = models.CharField(
        max_length=2,
        choices=CONDITION_CHOICES,
        default=NEW
    )

    seller = models.ForeignKey(SiteUser, related_name='seller')
    buyer = models.ForeignKey(SiteUser, related_name='buyer', null=True)

class Recommendations(models.Model):
    Page_id = models.IntegerField(primary_key=True)
    Related_pages = models.CharField(max_length=200)
