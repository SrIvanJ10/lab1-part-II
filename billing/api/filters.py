import django_filters
from django.db import models
from ..models import Invoice, Provider

from ..models import Invoice, Provider, Barrel


        
class InvoiceFilter(django_filters.FilterSet):
    invoice_no = django_filters.CharFilter(lookup_expr="icontains")
    issued_on = django_filters.DateFromToRangeFilter()

    provider = django_filters.NumberFilter(field_name="lines__barrel__provider")

    class Meta:
        model = Invoice
        fields = ["invoice_no", "issued_on", "provider"]


class ProviderFilter(django_filters.FilterSet):
    has_barrels_to_bill = django_filters.BooleanFilter(method='filter_has_barrels_to_bill')

    class Meta:
        model = Provider
        fields = []

    def filter_has_barrels_to_bill(self, queryset, name, value):
        if value:
            # Filter providers that have barrels where sum(invoice_lines.liters) < barrel.liters
            # OR where invoice_lines is null (no invoices yet)
            return queryset.annotate(
                total_billed_liters=models.Sum("barrels__invoice_lines__liters")
            ).filter(
                models.Q(barrels__invoice_lines__isnull=True) |
                models.Q(barrels__liters__gt=models.F("barrels__invoice_lines__liters"))
            ).distinct()
        return queryset
