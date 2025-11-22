from django.db import models
from django.conf import settings


class HabitCategory(models.TextChoices):
    HEALTH = "health", "Health"
    WORK = "work", "Work"
    LEARNING = "learning", "Learning"
    FITNESS = "fitness", "Fitness"
    MENTAL_HEALTH = "mental_health", "Mental Health"
    PRODUCTIVITY = "productivity", "Productivity"
    OTHER = "other", "Other"


class HabitFrequency(models.TextChoices):
    DAILY = "daily", "Daily"
    WEEKLY = "weekly", "Weekly"


class Habit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=20,
        choices=HabitCategory.choices,
        default=HabitCategory.OTHER
    )
    frequency = models.CharField(
        max_length=10,
        choices=HabitFrequency.choices,
        default=HabitFrequency.DAILY
    )
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} - {self.name}"


class HabitCheckIn(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="check_ins")
    date = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"{self.habit.name} - {self.date}"

