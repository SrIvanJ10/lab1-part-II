import django_filters
from django.db import models
from ..models import Invoice, Provider, Barrel

class InvoiceFilter(django_filters.FilterSet):
    invoice_no = django_filters.CharFilter(lookup_expr="icontains")
    issued_on = django_filters.DateFromToRangeFilter()

    # Enable filtering by provider ID on invoices
    provider = django_filters.NumberFilter(field_name="provider")

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
            # logic to filter providers with unbilled barrels
            # We can use the property/method reasoning or annotating
            # Since has_barrels_to_bill logic in model is complex to translate to single ORM call without valid annotation,
            # we try to check if there are barrels that are NOT totally billed.
            
            # Using the logic from the user's model method:
            return queryset.annotate(
                 billed_sum=models.Sum("barrels__invoice_lines__liters"),
                 total_liters=models.Sum("barrels__liters")
            ).filter(
                models.Q(barrels__invoice_lines__isnull=True) |
                models.Q(billed_sum__lt=models.F("barrels__liters"))
            ).distinct()
        return queryset


class BarrelFilter(django_filters.FilterSet):
    oil_type = django_filters.ChoiceFilter(choices=Barrel.OilType.choices)

    class Meta:
        model = Barrel
        fields = ["oil_type"]
