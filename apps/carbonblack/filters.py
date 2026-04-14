import django_filters
from .models import CBRule
from apps.escu.models import PIPELINE_STAGES
from apps.core.models import Tag

class CBRuleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Rule Name")
    description = django_filters.CharFilter(lookup_expr="icontains", label="Description")
    query = django_filters.CharFilter(lookup_expr="icontains", label="CB Query")
    mitre_tactic = django_filters.CharFilter(lookup_expr="icontains", label="MITRE Tactic")
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
    is_from_escu = django_filters.BooleanFilter(
        field_name="source_escu_rule", lookup_expr="isnull",
        label="Derived from ESCU?", exclude=True
    )
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())

    class Meta:
        model = CBRule
        fields = []
