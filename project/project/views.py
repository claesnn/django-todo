from django_filters import rest_framework as filters
from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer


class ProjectFilter(filters.FilterSet):
    technology = filters.TypedChoiceFilter(choices=Project.Technology.choices)
    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter
    queryset = Project.objects.all()
