from django_filters import FilterSet
from .models import Car, Rating


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'price': ['gt', 'lt'],
            'city': ['exact'],
            'country': ['exact'],
            'availability': ['exact'],
            'year': ['gt', 'lt'],
            'add_date': ['gt', 'lt']

        }


class RatingFilter(FilterSet):
    class Meta:
        model = Rating
        fields = {
            'stars': ['gt','lt']
        }
