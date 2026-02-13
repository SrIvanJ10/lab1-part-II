import django_filters
from ..models import Invoice, Barrel


        
class InvoiceFilter(django_filters.FilterSet):
    invoice_no = django_filters.CharFilter(lookup_expr="icontains")
    issued_on = django_filters.DateFromToRangeFilter()

    provider = django_filters.NumberFilter(field_name="lines__barrel__provider")

    class Meta:
        model = Invoice
        fields = ["invoice_no", "issued_on", "provider"]
        
class BarrelFilter(django_filters.FilterSet):
    oil_type = django_filters.CharFilter(
        field_name="oil_type",
        lookup_expr="icontains"
    )

    class Meta:
        model = Barrel
        fields = ["oil_type"]
