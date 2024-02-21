# views.py
from rest_framework import generics
from rest_framework.generics import ListCreateAPIView
from dmirs.models import DataFile
from dmirs.serializers import DataFileSerializer

from dmirs.models import Client

from backend_main.mixins.paginate import PaginateMixin


class DataFileListCreateView(PaginateMixin, generics.ListCreateAPIView):
    queryset = DataFile.objects.all()
    serializer_class = DataFileSerializer
    authentication_classes = []
    permission_classes = []

    def get_queryset(self):
        # Get the db_identifier from the request
        db_identifier = self.request.GET.get('db_identifier')
        client = Client.objects.filter(db_id=db_identifier).first()
        if client:
            # Filter DataFile queryset based on the client
            return DataFile.objects.filter(client=client)
        # If client is not found, return an empty queryset or handle as needed
        return DataFile.objects.none()

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
