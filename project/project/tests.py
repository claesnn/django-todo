from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project
from .serializers import ProjectSerializer


class ProjectViewSetTests(APITestCase):
    def setUp(self):
        self.project1 = Project.objects.create(
            title="Project 1",
            description="Description 1",
            technology=Project.Technology.PYTHON,
        )
        self.project2 = Project.objects.create(
            title="Project 2",
            description="Description 2",
            technology=Project.Technology.DJANGO,
        )

    def test_list_projects(self):
        url = reverse("projects-list")
        response = self.client.get(url)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_project(self):
        url = reverse("projects-detail", args=[self.project1.id])
        response = self.client.get(url)
        serializer = ProjectSerializer(self.project1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_project(self):
        url = reverse("projects-list")
        data = {
            "title": "Project 3",
            "description": "Description 3",
            "technology": Project.Technology.REACT,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 3)
        self.assertEqual(Project.objects.get(id=response.data["id"]).title, "Project 3")

    def test_update_project(self):
        url = reverse("projects-detail", args=[self.project1.id])
        data = {
            "title": "Updated Project 1",
            "description": "Updated Description 1",
            "technology": Project.Technology.FLUTTER,
        }
        response = self.client.put(url, data, format="json")
        self.project1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.project1.title, "Updated Project 1")

    def test_delete_project(self):
        url = reverse("projects-detail", args=[self.project1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Project.objects.count(), 1)
