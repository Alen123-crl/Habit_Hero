from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models.profile_model import Profile
from ..validations.validation import validate_email as validate_email_func, validate_name, validate_age, validate_image_url

User = get_user_model()


class UserUpdateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(required=False, validators=[validate_name])
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[validate_name]
    )
    age = serializers.IntegerField(required=False, validators=[validate_age])
    pro_pic = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[validate_image_url]
    )

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "age",
            "pro_pic",
        ]

    def validate_email(self, value):
        return validate_email_func(value, instance=self.instance)
    def update(self, instance, validated_data):
        profile = getattr(instance, 'profile', None)

        if 'email' in validated_data:
            instance.email = validated_data['email']
            instance.save()

        if profile:
            profile.first_name = validated_data.get('first_name', profile.first_name)
            profile.last_name = validated_data.get('last_name', profile.last_name)
            profile.age = validated_data.get('age', profile.age)
            profile.pro_pic = validated_data.get('pro_pic', profile.pro_pic)
            profile.save()

        return instance
