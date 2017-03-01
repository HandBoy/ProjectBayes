from rest_framework import viewsets
from core.models import BaysianNet, LogSession, GameSession
from .serializers import BaysianNetSerializer, LogSessionSerializer, GameSessionSerializer
from rest_framework.decorators import detail_route
# Create your views here.


class BaysianNetViewSet(viewsets.ModelViewSet):
    queryset = BaysianNet.objects.all()
    serializer_class = BaysianNetSerializer


class LogSessionViewSet(viewsets.ModelViewSet):
    queryset = LogSession.objects.all()
    serializer_class = LogSessionSerializer
    # For POST Requests
    def perform_create(self, serializer):
        serializer.save(score=777)


class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer

