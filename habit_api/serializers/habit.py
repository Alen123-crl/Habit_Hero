from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from ..models.habit_model import Habit, HabitCheckIn, HabitCategory, HabitFrequency
from ..validations.validation import validate_habit_name, validate_habit_name_update, validate_start_date, validate_habit_description


class HabitCheckInSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitCheckIn
        fields = "__all__"

class HabitSerializer(serializers.ModelSerializer):
    check_ins = HabitCheckInSerializer(many=True, read_only=True)
    best_days = serializers.SerializerMethodField()
    current_streak = serializers.SerializerMethodField()
    longest_streak = serializers.SerializerMethodField()
    success_rate = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            "id",
            "name",
            "description",
            "category",
            "frequency",
            "start_date",
            "best_days",
            "is_active",
            "created_at",
            "updated_at",
            "check_ins",
            "current_streak",
            "longest_streak",
            "success_rate",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    # streaks
    def get_current_streak(self, obj):
        from django.db.models.functions import TruncDate
        from datetime import timedelta
        today = timezone.now().date()
        streak = 0

        dates = (
            obj.check_ins.annotate(d=TruncDate("timestamp"))
            .values_list("d", flat=True)
            .distinct()
        )

        expected = today
        while expected in dates:
            streak += 1
            expected -= timedelta(days=1)

        return streak

    #get longest streak
    def get_longest_streak(self, obj):
        from django.db.models.functions import TruncDate
        from datetime import timedelta

        dates = (
            obj.check_ins.annotate(d=TruncDate("timestamp"))
            .values_list("d", flat=True)
            .distinct()
            .order_by("d")
        )

        if not dates:
            return 0

        longest = 1
        current = 1

        for i in range(1, len(dates)):
            if dates[i] - dates[i - 1] == timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        return longest

    # success rate
    def get_success_rate(self, obj):
        today = timezone.now().date()
        total_days = (today - obj.start_date).days + 1

        if total_days <= 0:
            return 0.0

        days_with_checkins = (
            obj.check_ins.values_list("date", flat=True).distinct().count()
        )

        if obj.frequency == HabitFrequency.DAILY:
            expected_days = total_days
        else:  # weekly
            expected_days = ((today - obj.start_date).days // 7) + 1

        if expected_days == 0:
            return 0.0

        return round((days_with_checkins / expected_days) * 100, 2)


    # best days (multiple)
    def get_best_days(self, obj):
        from django.db.models import Count

        daily_counts = (
            obj.check_ins.values("date")
            .annotate(total=Count("id"))
            .order_by("-total", "date")
        )

        if not daily_counts:
            return []

        max_count = daily_counts[0]["total"]

        return [
            {"date": entry["date"], "count": entry["total"]}
            for entry in daily_counts
            if entry["total"] == max_count
        ]


class HabitCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(validators=[validate_habit_name])
    start_date = serializers.DateField(validators=[validate_start_date])

    class Meta:
        model = Habit
        fields = [
            "name",
            "description",
            "category",
            "frequency",
            "start_date",
        ]


class HabitUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, validators=[validate_habit_name_update])

    class Meta:
        model = Habit
        fields = [
            "name",
            "description",
            "category",
            "frequency",
            "start_date",
            "is_active",
        ]

