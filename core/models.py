from django.db import models

# Create your models here.

class BaysianNet(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    text = models.TextField(verbose_name='Postagem', help_text='Informações')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ######################################
# Proficiency Model
# defines one or more variables related to the knowledge,
# skills, and abilities we wish to measure.
class Competence(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    text = models.TextField(verbose_name='Postagem', help_text='Informações')
    baysianet = models.ForeignKey('BaysianNet', related_name='competency')
    competencs = models.ManyToManyField('Competence', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Variable(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    value = models.IntegerField(verbose_name='Valor', help_text='Valor da variável', blank=True)
    competence = models.ForeignKey('Competence')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ######################################
# Struture for expressing multidimensional relationships
class Hierarchy(models.Model):
    baysianet = models.ForeignKey('BaysianNet')
    competency = models.ForeignKey('Competence')
    root = models.BooleanField(default=False)

    def __str__(self):
        return self.competency.title

class HierarchyFather(models.Model):
    father = models.ForeignKey(Hierarchy, related_name='father')
    child = models.ForeignKey(Hierarchy, related_name='child')



# ######################################
# Models for resolve sessions user and
# ######################################
class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    text = models.TextField(verbose_name='Postagem', help_text='Informações')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GameSession(models.Model):
    game = models.ForeignKey('Game')                            # Game id
    user = models.ForeignKey('auth.User', related_name='game_session')                       # user id  que starded the session
    goal = models.IntegerField(verbose_name='Objetivo', null=True, blank=True)
    score = models.IntegerField(verbose_name='Resultado Final', null=True, blank=True) #Final result of the session
    finish = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)


class LogSession(models.Model):
    user = models.ForeignKey('auth.User', related_name='log_session') # user id  que starded the session
    game = models.ForeignKey('Game')                            # Game id
    session = models.ForeignKey('GameSession')
    type_log = models.ForeignKey('TypeLogSession')                            # Game id
    expected = models.IntegerField(verbose_name='Resultado esperado', null=True, blank=True)
    result = models.IntegerField(verbose_name='Resultado Alcançado', null=True, blank=True)
    score = models.IntegerField(verbose_name='Pontuação', null=True, blank=True)
    data = models.CharField(max_length=255, verbose_name='Dados', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class TypeLogSession(models.Model):
    value = models.IntegerField(verbose_name='Valor')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

