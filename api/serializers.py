from rest_framework import serializers
from core.models import BaysianNet, LogSession, GameSession


class BaysianNetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaysianNet
        fields = ('title', 'created_date')


class LogSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogSession
        fields = '__all__'


class GameSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = ('game', 'user', 'goal', 'score', 'finish')


