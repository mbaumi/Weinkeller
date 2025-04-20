from django.db import models
import uuid

class Wine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100)
    winename = models.CharField(max_length=200)
    year = models.CharField(max_length=4, blank=True, null=True)
    alcohol = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, blank=True, null=True)
    wineryName = models.CharField(max_length=200, blank=True, null=True)
    wineryLocation = models.CharField(max_length=200, blank=True, null=True)
    wineryWebsite = models.URLField(blank=True, null=True)
    originCountry = models.CharField(max_length=100, blank=True, null=True)
    originRegion = models.CharField(max_length=100, blank=True, null=True)
    merchantName = models.CharField(max_length=200, blank=True, null=True)
    merchantWebsite = models.URLField(blank=True, null=True)
    tastingnotes = models.TextField(blank=True, null=True)
    bottlesbought = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.winename} ({self.year})"

class Tasting(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wine = models.ForeignKey(Wine, related_name='tastings', on_delete=models.CASCADE)
    tastingdate = models.DateTimeField()
    degurating = models.IntegerField(null=True, blank=True)
    degunotes = models.TextField(blank=True, null=True)
    foodpairing = models.TextField(blank=True, null=True)
    bottlesDrunken = models.IntegerField(default=0)

    def __str__(self):
        return f"Tasting of {self.wine.winename} on {self.tastingdate}"
