import time

from django_filters import rest_framework as filters
from django_tasks import task
from rest_framework import viewsets

from .models import Project
from .serializers import ProjectSerializer


@task()
def project_viewed(project_id: int) -> int:
    print(f"Called form DB worker, Project {project_id} viewed")
    return f"Project {project_id} viewed"


class ProjectFilter(filters.FilterSet):
    technology = filters.TypedChoiceFilter(choices=Project.Technology.choices)
    title = filters.CharFilter(lookup_expr="icontains")
    description = filters.CharFilter(lookup_expr="icontains")


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    filterset_class = ProjectFilter
    queryset = Project.objects.all()

    def retrieve(self, request, *args, **kwargs):
        print(kwargs["pk"])
        result = project_viewed.enqueue(kwargs["pk"])

        time.sleep(0.5)

        print(project_viewed.get_result(result.id).db_result.return_value)

        return super().retrieve(request, *args, **kwargs)
