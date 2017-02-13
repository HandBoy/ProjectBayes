from django.shortcuts import render
from rest_framework import viewsets

# Create your views here.

class LogSessionViewSet(viewsets.ModelViewSet):
    queryset = LogSession.objects.all()
    serializer_class = LogSessionSerializer
