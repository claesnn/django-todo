from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Todo, User
from .serializers import TodoSerializer, UserSerializer


class TodoViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            user=self.user, title="Test Todo", completed=False
        )
        self.url = reverse("todos-list")

    def test_list_todos(self):
        response = self.client.get(self.url)
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_todo(self):
        data = {"title": "New Todo", "completed": False}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(Todo.objects.get(id=response.data["id"]).title, "New Todo")

    def test_retrieve_todo(self):
        url = reverse("todos-detail", args=[self.todo.id])
        response = self.client.get(url)
        todo = Todo.objects.get(id=self.todo.id)
        serializer = TodoSerializer(todo)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_todo(self):
        url = reverse("todos-detail", args=[self.todo.id])
        data = {"title": "Updated Todo", "completed": True}
        response = self.client.put(url, data)
        self.todo.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.todo.title, "Updated Todo")
        self.assertEqual(self.todo.completed, True)

    def test_delete_todo(self):
        url = reverse("todos-detail", args=[self.todo.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)


class UserViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass", email="testuser@example.com"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users-list")

    def test_list_users(self):
        response = self.client.get(self.url)
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_user(self):
        data = {
            "username": "newuser",
            "password": "newpass",
            "email": "newuser@example.com",
            "groups": [],
            "user_permissions": [],
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=response.data["id"]).username, "newuser")

    def test_retrieve_user(self):
        url = reverse("users-detail", args=[self.user.id])
        response = self.client.get(url)
        user = User.objects.get(id=self.user.id)
        serializer = UserSerializer(user)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_user(self):
        url = reverse("users-detail", args=[self.user.id])
        data = {"username": "updateduser"}
        response = self.client.patch(url, data)
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, "updateduser")

    def test_delete_user(self):
        url = reverse("users-detail", args=[self.user.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
