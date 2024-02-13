from django.urls import path
from .views import *

urlpatterns = [
    path("db/project_data/", get_project_data, name="project_data"),
    path("db/hours_logged_this_month/", get_hours_logged_this_month, name="hours_logged_this_month"),
    path("db/closed_tickets_last_day/", get_closed_tickets_last_day, name="closed_tickets_last_day"),
    path("db/head_count/", get_head_count, name="head_count"),
    path("db/employee_hours_ratio/", get_employee_hours_ratio, name="employee_hours_ratio"),
    path("db/top_project_projection/", get_top_project_projection, name="top_project_projection"),
    path("db/projects_status_stats/", get_projects_status_stats, name="projects_status_stats"),
    path("db/current_month_projection/", get_current_month_projection, name="current_month_projection"),
    path("db/month_over_month/", get_month_over_month, name="month_over_month"),
]
