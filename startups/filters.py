import django_filters
from .models import Startup

class StartupFilter(django_filters.FilterSet):
    min_funding = django_filters.NumberFilter(field_name='funding_needed', lookup_expr='gte')
    max_funding = django_filters.NumberFilter(field_name='funding_needed', lookup_expr='lte')

    class Meta:
        model = Startup
        fields = ['category', 'min_funding', 'max_funding']
