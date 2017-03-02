
from rest_framework import viewsets
from core.models import BaysianNet, LogSession, GameSession, TablePoints
from .serializers import BaysianNetSerializer, LogSessionSerializer, GameSessionSerializer

# Create your views here.


class BaysianNetViewSet(viewsets.ModelViewSet):
    queryset = BaysianNet.objects.all()
    serializer_class = BaysianNetSerializer


class LogSessionViewSet(viewsets.ModelViewSet):
    queryset = LogSession.objects.all()
    serializer_class = LogSessionSerializer

    def perform_create(self, serializer):
        logData = self.request.data
        print(logData)
        point = TablePoints.objects.get(id=logData['table_points'])
        score = point.score
        if logData['type_log'] == '2':
            logs = LogSession.objects.filter(session=logData['session'])
            scoreLog = 0
            for log in logs:
                if log.type_log.value == 3:
                    scoreLog += log.score
                    print(scoreLog)
                elif log.type_log.value == 4:
                    scoreLog -= log.score
                    print(scoreLog)
            session = GameSession.objects.get(id=logData['session'])
            session.score = scoreLog
            session.save()
            print(scoreLog)

        serializer.save(score=score)


class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer


