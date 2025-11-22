from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import date
from ..models.habit_model import Habit, HabitCheckIn
from ..serializers.habit import (
    HabitSerializer,
    HabitCreateSerializer,
    HabitUpdateSerializer,
    HabitCheckInSerializer,
)


class HabitListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        habits = Habit.objects.filter(user=request.user, is_active=True)
        serializer = HabitSerializer(habits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HabitCreateSerializer(data=request.data)
        if serializer.is_valid():
            habit = serializer.save(user=request.user)
            response_serializer = HabitSerializer(habit)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            serializer = HabitSerializer(habit)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Habit.DoesNotExist:
            return Response(
                {"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            serializer = HabitUpdateSerializer(habit, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_serializer = HabitSerializer(habit)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Habit.DoesNotExist:
            return Response(
                {"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            habit.is_active = False
            habit.save()
            return Response(
                {"message": "Habit deleted successfully"}, status=status.HTTP_200_OK
            )
        except Habit.DoesNotExist:
            return Response(
                {"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND
            )


class HabitCheckInView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user, is_active=True)

            if habit.start_date > date.today():
                return Response(
                    {"error": "Cannot check in before the habit start date"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            note = request.data.get("notes", "")

            check_in = HabitCheckIn.objects.create(
                habit=habit,
                notes=note
            )

            return Response(
                HabitCheckInSerializer(check_in).data,
                status=status.HTTP_201_CREATED
            )

        except Habit.DoesNotExist:
            return Response({"error": "Habit not found"}, status=404)

    def get(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            check_ins = habit.check_ins.all()
            serializer = HabitCheckInSerializer(check_ins, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Habit.DoesNotExist:
            return Response(
                {"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND
            )


class HabitAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, habit_id):
        try:
            habit = Habit.objects.get(id=habit_id, user=request.user)
            serializer = HabitSerializer(habit)

            check_ins = habit.check_ins.all()

            # Count check-ins by day of week
            day_counts = {}
            for check_in in check_ins:
                day_name = check_in.date.strftime("%A")
                day_counts[day_name] = day_counts.get(day_name, 0) + 1

            # Best days = days you check-in most
            best_days = []
            if day_counts:
                max_count = max(day_counts.values())
                best_days = [
                    day for day, count in day_counts.items()
                    if count == max_count
                ]

            analytics = {
                "current_streak": serializer.data["current_streak"],
                "longest_streak": serializer.data["longest_streak"],
                "success_rate": serializer.data["success_rate"],
                "total_check_ins": check_ins.count(),
                "best_days": best_days,
                "day_distribution": day_counts,
                "category": habit.category,
            }

            return Response(analytics, status=status.HTTP_200_OK)

        except Habit.DoesNotExist:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)


class HabitOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        habits = Habit.objects.filter(user=user, is_active=True)
        total_habits = habits.count()

        # All check-ins for this user
        checkins = HabitCheckIn.objects.filter(habit__user=user)

        total_check_ins = checkins.count()

        # Today's metrics
        today_habits = habits.filter(frequency="daily")
        today_completed = checkins.filter(date=today, habit__in=today_habits).count()
        today_total = today_habits.count()
        today_completion_rate = round((today_completed / today_total) * 100, 2) if today_total else 0

        # Category distribution
        category_distribution = habits.values("category").annotate(count=Count("id")).order_by("-count")

        # Global longest streak (max of all habits)
        longest_streak = max([HabitSerializer(h).data["longest_streak"] for h in habits], default=0)

        # Average success rate across all habits
        avg_success_rate = round(
            sum([HabitSerializer(h).data["success_rate"] for h in habits]) / total_habits, 2
        ) if total_habits else 0

        # Best overall days (multiple)
        daily_counts = checkins.values("date").annotate(total=Count("id")).order_by("-total")
        best_days = []
        if daily_counts:
            max_count = daily_counts[0]["total"]
            best_days = [{"date": d["date"], "count": d["total"]} for d in daily_counts if d["total"] == max_count]

        overview = {
            "total_habits": total_habits,
            "total_check_ins": total_check_ins,
            "today_total": today_total,
            "today_completed": today_completed,
            "today_completion_rate": today_completion_rate,
            "category_distribution": list(category_distribution),
            "habits_by_category": list(category_distribution),
            "longest_streak": longest_streak,
            "avg_success_rate": avg_success_rate,
            "best_days": best_days,
        }

        return Response(overview)


