import os

from django.contrib.auth.models import User
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from literatures_and_datum_management.models import DocumentSourceTable, LiteratureDataTable, UserLexicon
from literatures_and_datum_management.serializers import DocumentSourceModelSerializer
from literatures_and_datum_management.serializers import LiteratureDataModelSerializer
from literatures_and_datum_management.serializers import UserLexiconModelSerializer


class DocumentSourceModelViewSet(ModelViewSet):
    queryset = DocumentSourceTable.objects.all()
    serializer_class = DocumentSourceModelSerializer


class LiteratureDataModelViewSet(ModelViewSet):
    queryset = LiteratureDataTable.objects.all()
    serializer_class = LiteratureDataModelSerializer


class UserLexiconModelViewSet(ModelViewSet):
    queryset = UserLexicon.objects.all()
    serializer_class = UserLexiconModelSerializer


class DocDownloadAPIView(APIView):
    def get(self, request, pk):
        def file_iterator(filename, chunk_size=512):
            with open(filename, 'rb') as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break

        doc_obj = DocumentSourceTable.objects.get(pk=pk)
        file_path = os.path.join('./media/', str(doc_obj.upload))
        file_name = str(doc_obj.liter_name)

        response = StreamingHttpResponse(file_iterator(file_path))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}'.format(file_name + '.pdf')
        return response
