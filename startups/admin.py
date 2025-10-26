from django.contrib import admin
from .models import Startup

@admin.register(Startup)
class StartupAdmin(admin.ModelAdmin):
    list_display = ('title', 'founder', 'category', 'funding_needed', 'created_at')
    search_fields = ('title', 'description', 'founder__username')
