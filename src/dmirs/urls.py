from django.urls import path
from dmirs.views.TenementView import TenementView
from dmirs.views.QualifiedDataView import QualifiedDataView

from dmirs.views.ConfigView import ConfigView

urlpatterns = [
    path('initialize-config/', ConfigView.as_view(), name='initialize-config'),
    path('tenement/', TenementView.as_view(), ),
    path('qualified-data/', QualifiedDataView.as_view(), ),

    # api endpoints
]
