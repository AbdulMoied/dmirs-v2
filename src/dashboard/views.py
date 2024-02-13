from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.db.models import Count, Sum
from projects.models import Project
from .clickup_suit import *
import calendar


# Active Projects, Total Projects, Total Clients
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_project_data(request):
    return Response(
        {
            "total_active_project_count": Project.objects.filter(status="In Development").count(),
            "total_project_count": Project.objects.all().count(),
            "client_count": Project.objects.all().count(),
        },
        status=status.HTTP_200_OK
    )


# Hours Logged (current month)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_hours_logged_this_month(request):
    return Response(hours_logged_this_month(), status=status.HTTP_200_OK)


# Closed Tickets last 24 hours
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_closed_tickets_last_day(request):
    return Response(closed_tickets_last_day(), status=status.HTTP_200_OK)


# Employee Head Count
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_head_count(request):
    return Response(head_count(), status=status.HTTP_200_OK)


# Budget vs Actual hours' projection per month
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_current_month_projection(request):
    current_month_start = datetime.now() - timedelta(days=int(datetime.now().day) - 1)
    curr_datetime = datetime.now()
    days_in_month = int(calendar.monthrange(curr_datetime.year, curr_datetime.month)[1])

    budget_distribution = Project.objects.filter(start_date__range=[current_month_start, datetime.now()]).aggregate(
        Sum('budget'))
    total_time_duration = budget_distribution['budget__sum'] / days_in_month
    sunset_projection_list = [{
        "day": day_t,
        # "month": curr_datetime.month,
        # "year": curr_datetime.year,
        "total_time_duration": total_time_duration
    } for day_t in range(1, int(curr_datetime.day) + 1)]

    #
    # sunset_projection = recent_projects.values('start_date__day', 'start_date__month', 'start_date__year') \
    #     .annotate(total_time_duration=Sum('budget') / days_in_month).order_by('-start_date__year', '-start_date__month',
    #                                                                           '-start_date__day')

    # sunset_projection_list = [
    #     {
    #         "day": entry['start_date__day'],
    #         "month": entry['start_date__month'],
    #         "year": entry['start_date__year'],
    #         "total_time_duration": entry['total_time_duration']
    #     }
    #     for entry in sunset_projection
    # ]

    return Response({
        "clickup_projection": current_month_projection(),
        "sunset_projection": sunset_projection_list,

    }, status=status.HTTP_200_OK)


# Top 10 Projects (in terms of budget) Projected vs Actual Hours (whole project)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_top_project_projection(request):
    return Response(top_project_projection(), status=status.HTTP_200_OK)


# highest and lowest 10 Employee month level bases of Hours Logged
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_employee_hours_ratio(request):
    return Response(employee_hours_ratio(), status=status.HTTP_200_OK)


# Project Started Month Over Month
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_month_over_month(request):
    six_months_ago = datetime.now() - timedelta(days=6 * 30)
    recent_projects = Project.objects.filter(start_date__range=[six_months_ago, datetime.now()])

    sunset_projection = recent_projects.values('start_date__month', 'start_date__year') \
        .annotate(count=Count('id')).order_by('-start_date__year', '-start_date__month')

    sunset_projection_list = [
        {
            "month": entry['start_date__month'],
            "year": entry['start_date__year'],
            "count": entry['count']
        }
        for entry in sunset_projection
    ]

    return Response({
        "sunset_projection": sunset_projection_list,

    }, status=status.HTTP_200_OK)


# Project Status total
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_projects_status_stats(request):
    project_data = Project.objects.values('status').annotate(count=Count('status')).order_by('-count')
    return Response(list(project_data), status=status.HTTP_200_OK)
