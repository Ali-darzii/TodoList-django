from rest_framework import serializers

from auth_service.models import UserLogins
from todo.models import Todo


class TodosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"
        read_only_fields = ["user_logins"]

    def create(self, validated_data):
        user_logins = self.context.get("request").user.user_logins
        return Todo.objects.create(user_logins=user_logins, **validated_data)
