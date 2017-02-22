from rest_framework import viewsets
from core.models import BaysianNet, LogSession, GameSession
from .serializers import BaysianNetSerializer, LogSessionSerializer, GameSessionSerializer
# Create your views here.


class BaysianNetViewSet(viewsets.ModelViewSet):
    queryset = BaysianNet.objects.all()
    serializer_class = BaysianNetSerializer


class LogSessionViewSet(viewsets.ModelViewSet):
    queryset = LogSession.objects.all()
    serializer_class = LogSessionSerializer


class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

