import django_filters
from django import forms
from .models import ESCURule, PIPELINE_STAGES
from apps.core.models import Tag

ANALYST_CHOICES = [
    ("analyst_1", "Analyst 1"), ("analyst_2", "Analyst 2"),
    ("analyst_3", "Analyst 3"), ("analyst_4", "Analyst 4"),
    ("analyst_5", "Analyst 5"),
]

class ESCURuleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Rule Name")
    description = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    search_spl = django_filters.CharFilter(
        field_name="search", lookup_expr="icontains", label="SPL Query"
    )
    mitre_tactic = django_filters.CharFilter(lookup_expr="icontains", label="MITRE Tactic")
    mitre_technique = django_filters.CharFilter(lookup_expr="icontains", label="MITRE Technique")
    mitre_technique_id = django_filters.CharFilter(lookup_expr="icontains", label="Technique ID")
    severity = django_filters.MultipleChoiceFilter(
        choices=[
            ("critical","Critical"), ("high","High"),
            ("medium","Medium"), ("low","Low"), ("informational","Informational")
        ],
        widget=django_filters.widgets.CSVWidget
    )
    status = django_filters.MultipleChoiceFilter(
        choices=PIPELINE_STAGES,
        widget=django_filters.widgets.CSVWidget
    )
    assigned_analyst = django_filters.ChoiceFilter(
        choices=[("", "All")] + ANALYST_CHOICES
    )
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    data_source = django_filters.CharFilter(lookup_expr="icontains", label="Data Source")
    has_cb_conversion = django_filters.BooleanFilter(
        method="filter_has_cb", label="Has CB Conversion?"
    )
    first_seen_after = django_filters.DateFilter(
        field_name="first_seen_batch__imported_at", lookup_expr="gte", label="First Seen After"
    )
    first_seen_before = django_filters.DateFilter(
        field_name="first_seen_batch__imported_at", lookup_expr="lte", label="First Seen Before"
    )

    def filter_has_cb(self, queryset, name, value):
        if value:
            return queryset.filter(cb_conversions__isnull=False).distinct()
        return queryset.filter(cb_conversions__isnull=True)

    class Meta:
        model = ESCURule
        fields = []
