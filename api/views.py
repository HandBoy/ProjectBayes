from django.shortcuts import render
from rest_framework import viewsets
from core.models import BaysianNet, LogSession
from .serializers import BaysianNetSerializer, LogSessinSerializer
# Create your views here.


class BaysianNetViewSet(viewsets.ModelViewSet):
    queryset = BaysianNet.objects.all()
    serializer_class = BaysianNetSerializer

class LogSessionViewSet(viewsets.ModelViewSet):
    queryset = LogSession.objects.all()
    serializer_class = LogSessinSerializer