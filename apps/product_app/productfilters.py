from django_filters import FilterSet
import django_filters as filters
from .models import product
class productfilter(FilterSet):
    BOOLEAN_CHOICES = ((0, 'Out Of Stock'), (1, 'In Stock'),)
    product_name = filters.CharFilter(field_name='p_name', lookup_expr='icontains', label='Product Name:')
    in_stock = filters.ChoiceFilter(field_name='p_is_active',choices=BOOLEAN_CHOICES, label='In Stock:')
    class Meta:
        model = product
        fields = []
