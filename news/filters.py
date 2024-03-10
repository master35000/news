from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from .models import Post, Category
from django.forms import DateTimeInput

class PostFilter(FilterSet):
    added_after = DateTimeFilter(
        field_name='datetime_in',
        lookup_expr='gt',
        label='Дата создания не ранее чем:',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )

    added_title = CharFilter(field_name = 'title', lookup_expr='icontains', label='Название статьи')

    added_pcategory = ModelChoiceFilter (field_name='pcategory', queryset=Category.objects.all(), label='Категория поста', empty_label='Все категории')

