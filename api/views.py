from django.http.response import Http404
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from core.models import BaysianNet, LogSession, GameSession, \
    TablePoints, CompetenceUser, ConditionalProbabilityTable
from .serializers import BaysianNetSerializer, LogSessionSerializer, \
    GameSessionSerializer, ConditionalProbabilitySerializer

# Create your views here.


class BaysianNetViewSet(viewsets.ModelViewSet):
    queryset = BaysianNet.objects.all()
    serializer_class = BaysianNetSerializer


class LogSessionViewSet(viewsets.ModelViewSet):
    queryset = LogSession.objects.all()
    serializer_class = LogSessionSerializer


    def perform_create(self, serializer):
        log_data = self.request.data
        point = TablePoints.objects.get(id=log_data['table_points'])
        score = point.score
        if log_data['type_log'] == 2: #Fim da sessão
            logs = LogSession.objects.filter(session=log_data['session'])
            score_log = 0
            for log in logs:
                if log.type_log.value == 3:
                    score_log += log.score
                elif log.type_log.value == 4:
                    score_log -= log.score
            session = GameSession.objects.get(id=log_data['session'])
            percent = (score_log*100)/session.goal
            if percent >= 90:
                level_id = 5
            elif percent >= 60:
                level_id = 6
            else:
                level_id = 7
            GameSession.objects.filter(id=log_data['session']).update(finish=True,
                                                                       score=score_log,
                                                                       percent_finish=percent,
                                                                       level_id=level_id)
            print(percent)
            competencs_log = LogSession.objects.filter(session=log_data['session']).filter(competency__isnull=False)\
                                                                                .values('competency').distinct()
            print(competencs_log)
            for comp_log in competencs_log:
                print(comp_log)
                log_comp = logs.filter(competency=comp_log['competency'])
                total = log_comp.count()
                acerto = 0
                for log in log_comp:
                    if log.type_log.value == 3:
                        acerto += 1

                percent = (acerto*100)/total
                print(percent)
                competenc_user = CompetenceUser()
                competenc_user.user = session.user
                competenc_user.game = session.game
                competenc_user.competency_id= comp_log['competency']
                if percent >= 90:
                    competenc_user.level_id = 5
                elif percent >= 60:
                    competenc_user.level_id = 6
                else:
                    competenc_user.level_id = 7

                competenc_user.save()
                print(competenc_user)



        elif log_data['type_log'] == 1:
            session = GameSession()
            session.user = log_data['user']
            session.game_id = log_data['game_id']
            session.finish = False
            session.save()
            serializer.save(score=score, session=session.id)
        else:
            serializer.save(score=score)


class GameSessionViewSet(viewsets.ModelViewSet):
    queryset = GameSession.objects.all()
    serializer_class = GameSessionSerializer


class ConditionalProbabilityViewSet(viewsets.ModelViewSet):
    queryset = ConditionalProbabilityTable.objects.all()
    serializer_class = ConditionalProbabilitySerializer
