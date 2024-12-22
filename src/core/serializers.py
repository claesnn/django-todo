from rest_framework import serializers

from core.models import Todo, User


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
        groups_data = validated_data.pop("groups", [])
        user_permissions_data = validated_data.pop("user_permissions", [])

        user = User.objects.create_user(**validated_data)

        user.groups.set(groups_data)
        user.user_permissions.set(user_permissions_data)

        return user
