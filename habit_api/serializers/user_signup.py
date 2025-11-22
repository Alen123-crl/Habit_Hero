from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models.profile_model import Profile
from ..validations.validation import validate_email, validate_name, validate_age, validate_image_url
from ..models.user_model import SignupMethod

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(write_only=True)

    first_name = serializers.CharField(validators=[validate_name])
    last_name = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
        validators=[validate_name],
    )
    age = serializers.IntegerField(validators=[validate_age])
    pro_pic = serializers.URLField(
        required=False,
        allow_null=True,
        validators=[validate_image_url],
    )

    signup_method = serializers.ChoiceField(
        choices=SignupMethod.choices,
        default=SignupMethod.MANUAL
    )

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "signup_method",
            "first_name",
            "last_name",
            "age",
            "pro_pic",
        ]

    def create(self, validated_data):

        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name", "")
        age = validated_data.pop("age")
        pro_pic = validated_data.pop("pro_pic", None)

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data.get("password"),
            signup_method=validated_data.get("signup_method"),
        )

        Profile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            age=age,
            pro_pic=pro_pic,
        )

        return user
