from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Todo, User
from .serializers import TodoSerializer, UserSerializer


class TodoFilter(filters.FilterSet):
    user = filters.NumberFilter()
    title = filters.CharFilter(lookup_expr="icontains")
    completed = filters.BooleanFilter()
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()
    project = filters.NumberFilter()

    class Meta:
        model = Todo
        fields = ["user", "title", "completed", "created_at", "updated_at", "project"]


class TodoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Todo model."""

    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Todo.objects.all()
    filterset_class = TodoFilter

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)


class UserViewset(viewsets.ModelViewSet):
    """ViewSet for the User model."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = {
        "email": ["exact"],
        "username": ["exact"],
        "first_name": ["exact"],
        "last_name": ["exact"],
        "is_active": ["exact"],
        "is_staff": ["exact"],
        "is_superuser": ["exact"],
        "date_joined": ["exact", "lte", "gte"],
    }
