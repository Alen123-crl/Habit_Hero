from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()
def validate_name(name):
    if len(name) < 3:
        raise ValidationError("Name must be at least 2 characters long.")

    if not re.match(r"^[A-Za-z]+$", name):
        raise ValidationError("Name must contain only alphabetic letters.")

    return name
def validate_email(email):
    user = User.objects.filter(email = email).exists()
    if user :
        raise ValidationError("Email already exists")

    return email


def validate_age(age):
    if age < 7 or age > 99:
        raise ValidationError("Age must be between 7 and 99.")
    return age


def validate_image_url(url):
    if url and not re.match(r"^https?://.*\.(jpg|jpeg|png|webp)$", url.lower()):
        raise ValidationError("Invalid image format.")

    return url
