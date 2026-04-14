import django_filters
from django import forms
from .models import ESCURule, PIPELINE_STAGES
class ESCURuleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains", label="Kural Adı", widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    status = django_filters.ChoiceFilter(choices=PIPELINE_STAGES, label="Durum", widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    class Meta:
        model = ESCURule
        fields = ['name', 'status']
