from django.urls import path
from dmirs.views.TenementView import TenementView
from dmirs.views.QualifiedDataView import QualifiedDataView

urlpatterns = [
    path('tenement/', TenementView.as_view(), ),
    path('qualified-data/', QualifiedDataView.as_view(), ),

    # api endpoints
]
