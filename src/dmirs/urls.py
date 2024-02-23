from django.urls import path, include
from dmirs.views.TenementView import TenementView
from dmirs.views.QualifiedDataView import QualifiedDataView
from dmirs.views.ConfigView import ConfigView
from dmirs.views.ConfigView import test_function

from dmirs.views.DataFileView import DataFileListCreateView

urlpatterns = [
    # api endpoints
    path('initialize-config/', ConfigView.as_view(), name='initialize-config'),
    path('tenement/', TenementView.as_view(), ),
    path('qualified-data/', QualifiedDataView.as_view(), ),
    path('data-files/', DataFileListCreateView.as_view(), name='datafile-list-create'),
    path('playground/', test_function, ),
]
