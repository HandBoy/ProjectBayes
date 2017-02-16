from rest_framework import serializers
from core.models import BaysianNet, LogSession

class BaysianNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaysianNet
        fields = ('title', 'created_date')


class LogSessinSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSession
        fields = ('type_log', 'user', 'game', 'expected','result', 'score', 'data')