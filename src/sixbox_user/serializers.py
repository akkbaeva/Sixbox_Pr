from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from sixbox_user.models import S_User


class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = S_User
        fields = ('username', 'number')


class User_Register_Serializer(serializers.ModelSerializer):
    number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=S_User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = S_User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'number',
                  'password',
                  'password2')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Password fields did not match.'})

        return attrs

    def create(self, validated_data):
        user = S_User.objects.create(
            username=validated_data['username'],
            number=validated_data['number']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class User_Login_Serializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, required=True)
    number = serializers.CharField(required=True)
    password = serializers.CharField(max_length=20, required=True, write_only=True)
