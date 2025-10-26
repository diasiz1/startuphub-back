from rest_framework import serializers
from .models import Investment

class InvestmentSerializer(serializers.ModelSerializer):
    investor_name = serializers.CharField(source='investor.username', read_only=True)
    investor_email = serializers.EmailField(source='investor.email', read_only=True)
    startup_title = serializers.CharField(source='startup.title', read_only=True)
    startup_founder = serializers.CharField(source='startup.founder.username', read_only=True)

    class Meta:
        model = Investment
        fields = [
            'id',
            'startup',
            'amount',
            'message',
            'created_at',
            'investor_name',
            'investor_email',
            'startup_title',
            'startup_founder'
        ]
        read_only_fields = ['id', 'created_at', 'investor_name', 'startup_title', 'startup_founder']

    def validate_startup(self, value):
        if not value:
            raise serializers.ValidationError("Startup ID is required.")
        return value

