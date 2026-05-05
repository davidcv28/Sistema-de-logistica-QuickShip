import django_filters
from django import forms
from QuickShipApp.domains.shipping.models import Shipping

####SHIPPING FILTER
class ShippingFilterSet(django_filters.FilterSet):
    tracking_code = django_filters.CharFilter(
        lookup_expr='iexact',
        field_name='tracking_code',
        label = 'Codigo de seguimiento',
        widget = forms.TextInput(attrs={'placeholder':'Escribe tu codigo de seguimiento aqui'})
    )
    class Meta:
        model = Shipping
        fields = ['tracking_code']