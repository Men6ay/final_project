from apps.users.tasks import send_message_to_email
from apps.users.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id', 'username', 'gender', 'age', 'password','email',
        )

    def create(self, validated_data):
        password = validated_data['password']
        email = validated_data['email']
        username = validated_data['username']
        gender = validated_data['gender']
        age = validated_data['age']
        user = User.objects.create(
            username=username,
            gender=gender,
            age=age,
            email=email,
        )
        user.is_active = False
        user.set_password(password)
        user.save()
        send_message_to_email.delay(user.email)
        return user
