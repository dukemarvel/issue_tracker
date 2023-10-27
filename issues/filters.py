import django_filters
from .models import Issue

class IssueFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    created_by = django_filters.NumberFilter(field_name="created_by")
    assigned_to = django_filters.NumberFilter(field_name="assigned_to")
    labels = django_filters.NumberFilter(field_name="labels", method="filter_by_labels")

    class Meta:
        model = Issue
        fields = ['title', 'created_by', 'assigned_to', 'labels']

    def filter_by_labels(self, queryset, name, value):
        return queryset.filter(labels__in=value.split(','))
