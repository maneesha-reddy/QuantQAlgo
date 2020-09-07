from django.db import models
from django.conf import settings
from django.utils import timezone


class BackTest(models.Model):
    symbol = models.CharField(max_length=200)
    from_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.to_date = timezone.now()
        self.from_date = timezone.now()
        self.save()
