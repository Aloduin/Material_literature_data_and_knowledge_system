from django.urls import path, re_path

from rest_framework import routers

from literatures_and_datum_management import views

routers = routers.SimpleRouter()
routers.register(r'literatures', views.DocumentSourceModelViewSet)
routers.register(r'datum', views.LiteratureDataModelViewSet)
routers.register(r'lexicons', views.UserLexiconModelViewSet)

urlpatterns = [
    re_path("^download_literatures/(?P<pk>\d+)/$", views.DocDownloadAPIView.as_view()),
]+routers.urls