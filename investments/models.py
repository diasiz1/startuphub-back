from django.db import models
from django.conf import settings
from startups.models import Startup

class Investment(models.Model):
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.investor.username} invested {self.amount} in {self.startup.title}"
