from apps.users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'gender', 'age', 'password','email',
        )

    def create(self, validated_data):
        user = super().create(validated_data)
        password = validated_data['password']
        user.set_password(password)
        user.save()
        return user

