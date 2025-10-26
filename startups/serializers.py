from decimal import Decimal
from django.db.models import Sum
from rest_framework import serializers
from .models import Startup
from comments.serializers import CommentSerializer


class StartupSerializer(serializers.ModelSerializer):
    # read-only fields pulled from related objects / computed
    founder = serializers.ReadOnlyField(source='founder.username')
    investments_count = serializers.SerializerMethodField()
    total_invested = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    recent_comments = CommentSerializer(many=True, read_only=True)


    class Meta:
        model = Startup
        fields = [
            'id',
            'title',
            'description',
            'demo_link',
            'funding_needed',
            'category',
            'founder',
            'created_at',

            # computed/read-only
            'investments_count',
            'total_invested',
            'comments_count',
            'recent_comments'
        ]
        read_only_fields = [
            'id', 'founder', 'created_at',
            'investments_count', 'total_invested', 'comments_count'
        ]

    def get_investments_count(self, obj):
        return obj.investments.count()

    def get_total_invested(self, obj):
        total = obj.investments.aggregate(total=Sum('amount'))['total']
        # return Decimal to keep consistent numeric type (DRF will render as string/number)
        return total or Decimal('0.00')

    def get_comments_count(self, obj):
        return obj.comments.count()

    def validate_funding_needed(self, value):
        if value is None:
            raise serializers.ValidationError("Funding needed is required.")
        if value < 0:
            raise serializers.ValidationError("Funding needed must be >= 0.")
        return value
    
    def get_recent_comments(self, obj):
        return CommentSerializer(obj.comments.all()[:3], many=True).data
