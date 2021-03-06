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
    #competencs = models.ManyToManyField('Competence', blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Variable(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    value = models.CharField(max_length=200, verbose_name='Valor', help_text='Valor da variável', blank=True)
    competence = models.ForeignKey(Competence, related_name='variable')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Struture for expressing multidimensional relationships
class Hierarchy(models.Model):
    baysianet = models.ForeignKey('BaysianNet')
    competency_father = models.ForeignKey(Competence, related_name='father')
    competency_child = models.ForeignKey(Competence, related_name='child')

    def __str__(self):
        return self.competency_father.title


class ConditionalProbabilityTable(models.Model):
    baysianet = models.ForeignKey('BaysianNet')
    competency_father = models.ForeignKey(Competence, related_name='cpt_father')
    variable_father = models.ForeignKey(Variable, related_name='father')
    variable_child = models.ForeignKey(Variable, related_name='child')
    value = models.CharField(max_length=200, verbose_name='Valor', help_text='Valor da variável', blank=True)
    line = models.IntegerField(verbose_name='Linha', null=True, blank=True)

    def __str__(self):
        return self.variable_father.competence.title

# ######################################
# Models for resolve sessions user
# ######################################
class Game(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    text = models.TextField(verbose_name='Postagem', help_text='Informações')
    competence = models.ManyToManyField(Competence)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class GameSession(models.Model):
    game = models.ForeignKey('Game')                            # Game id
    user = models.ForeignKey('auth.User', related_name='game_session')                       # user id  que starded the session
    goal = models.IntegerField(verbose_name='Objetivo', null=True, blank=True)
    score = models.IntegerField(verbose_name='Resultado Final', null=True, blank=True) #Final result of the session
    finish = models.BooleanField(default=False) # 0 false 1 true
    level = models.ForeignKey('TypeLogSession')
    percent_finish = models.FloatField(verbose_name='Percentual', default=0, null=True, blank=True) #Final result of the session
    created_date = models.DateTimeField(auto_now_add=True)


class LogSession(models.Model):
    user = models.ForeignKey('auth.User', related_name='user_session') # user id  que starded the session
    game = models.ForeignKey('Game')                            # Game id
    session = models.ForeignKey('GameSession', related_name='log_session')
    type_log = models.ForeignKey('TypeLogSession')                            # Game id
    expected = models.IntegerField(verbose_name='Resultado esperado', null=True, blank=True)
    result = models.IntegerField(verbose_name='Resultado Alcançado', null=True, blank=True)
    score = models.IntegerField(verbose_name='Pontuação', null=True, blank=True)
    data = models.CharField(max_length=255, verbose_name='Dados', null=True, blank=True)
    competency = models.ForeignKey('Competence', null=True, blank=True)
    table_points = models.ForeignKey('TablePoints')
    created_date = models.DateTimeField(auto_now_add=True)


class TypeLogSession(models.Model):
    value = models.IntegerField(verbose_name='Valor')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CompetenceUser(models.Model):
    game = models.ForeignKey('Game')
    competency = models.ForeignKey('Competence', null=True, blank=True)
    user = models.ForeignKey('auth.User')
    level = models.ForeignKey('TypeLogSession')
    created_date = models.DateTimeField(auto_now_add=True)

# ######################################
# Models for resolve sessions user and
# ######################################e
class TablePoints(models.Model):
    game = models.ForeignKey('Game')
    competency = models.ForeignKey('Competence', null=True, blank=True)
    type_log = models.ForeignKey('TypeLogSession', null=True, blank=True)
    rule = models.CharField(max_length=255, verbose_name='Regra')
    score = models.IntegerField(verbose_name='Pontuacao', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.rule + " " + self.type_log.name

