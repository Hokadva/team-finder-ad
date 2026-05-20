import django_filters

from core.consts import FILTER_CHOICES

from .models import User


class UserFilter(django_filters.FilterSet):
    filter = django_filters.ChoiceFilter(
        choices=FILTER_CHOICES,
        method='apply_filter'
    )

    class Meta:
        model = User
        fields = []

    def apply_filter(self, queryset, name, value):
        if not value or not self.request.user.is_authenticated:
            return queryset

        if value == FILTER_CHOICES[0][0]:
            return queryset.filter(
                owned_projects__in=self.request.user.favorites.all()
                ).distinct()

        elif value == FILTER_CHOICES[1][0]:
            return queryset.filter(
                owned_projects__in=self.request.user.participated_projects.
                all()).distinct()

        elif value == FILTER_CHOICES[2][0]:
            return queryset.filter(
                favorites__in=self.request.user.owned_projects.all()
                ).distinct()

        elif value == FILTER_CHOICES[3][0]:
            return queryset.filter(
                participated_projects__in=self.request.user.
                owned_projects.all()
                ).distinct()
        return queryset
