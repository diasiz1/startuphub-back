from django.db import models
from django.conf import settings

class Startup(models.Model):
    CATEGORY_CHOICES = [
        ('AI', 'Artificial Intelligence'),
        ('FinTech', 'Financial Technology'),
        ('GameDev', 'Game Development'),
        ('EdTech', 'Education Technology'),
    ]

    founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="startups")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    demo_link = models.URLField(blank=True, null=True)
    funding_needed = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.category})"

