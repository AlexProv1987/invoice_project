from django_filters import FilterSet
import django_filters as filters
from .models import product
class productfilter(FilterSet):
    product_name = filters.CharFilter(field_name='p_name', lookup_expr='icontains', label='Product Name: ')
    class Meta:
        model = product
        fields = []
