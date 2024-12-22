from core.models import Todo, User
from rest_framework import serializers


class TodoSerializer(serializers.ModelSerializer):
    """Serializer for the Todo model."""

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Todo
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""

    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["email"].read_only = True
        else:
            self.fields["email"].required = True

    def create(self, validated_data):
        """Create a user with a hashed password."""
        return User.objects.create_user(**validated_data)
