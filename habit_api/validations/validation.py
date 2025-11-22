from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from datetime import date
import re

User = get_user_model()

def validate_name(name):
    if len(name) < 3:
        raise ValidationError("Name must be at least 2 characters long.")

    if not re.match(r"^[A-Za-z]+$", name):
        raise ValidationError("Name must contain only alphabetic letters.")

    return name

def validate_email(email, instance=None):
    qs = User.objects.filter(email=email)
    if instance:
        qs = qs.exclude(pk=instance.pk) 

    if qs.exists():
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


def validate_habit_name(name):
    if len(name) > 200:
        raise ValidationError("Habit name is too long")
    return name.strip()

def validate_habit_description(description):
    if len(description) > 500:
        raise ValidationError("Habit description is too long")
    return description.strip()

def validate_habit_name_update(name):
    if name:
        if len(name.strip()) == 0:
            raise ValidationError("Habit name cannot be empty")
        return name.strip()
    return name

def validate_start_date(date):
    if date < date.today(): 
        raise ValidationError("Start date cannot be in the past")
    return date