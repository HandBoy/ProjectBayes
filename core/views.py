from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import BaysianNet, Competence, LogSession, Game, GameSession, CompetenceUser, Hierarchy, \
    ConditionalProbabilityTable, Variable
from core.forms import BaysianForm, CompetenceForm, VariableForm, RegistrationForm, HierarchyForm, \
    ConditionalProbabilityTableForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from itertools import product
from django.db.models import Count
from django.db.models import Q

import itertools


# Create your views here.
def index(request):
    context = {}
    context['nets'] = BaysianNet.objects.all()
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context['num_visits'] = num_visits
    return render(request, 'index.html', context)


@login_required
def baysianet_new(request):
    if request.method == "POST":
        form = BaysianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core.views.index')
    else:
        form = BaysianForm()
    return render(request, 'baysianet_edit.html', {'form': form})


def baysianet_detail(request, pk):
    context = {}
    rede = {}
    baysianet = get_object_or_404(BaysianNet, pk=pk)
    hierarchies = Hierarchy.objects.filter(baysianet=pk)
    father = hierarchies.distinct('competency_father')
    for pai in father.all():
        filhos = hierarchies.filter(competency_father=pai.competency_father_id)
        rede[pai.competency_father] = filhos.all()

    context['rede'] = rede
    context['baysianet'] = baysianet
    return render(request, 'net/baysianet_detail.html', context)


def competencies(request):
    context = {}
    context['competencia'] = Competence.objects.all()
    return render(request, 'competencies.html', context)


def competence_detail(request, pk):
    context = {}
    competence = get_object_or_404(Competence, pk=pk)
    context['competence'] = competence
    return render(request, 'net/baysianet_detail.html', context)


@login_required
def competence_new(request, baysianet_pk=None):
    baysianet = None
    hierarchy_list = []
    context = {}
    if baysianet_pk:
        baysianet = get_object_or_404(BaysianNet, pk=baysianet_pk)
        context['baysianet'] = baysianet

    if request.method == "POST":
        form = CompetenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('net_detail', baysianet_pk)
    else:
        form = CompetenceForm()
    return render(request, 'net/competence_new.html', {'form': form,
                                                       'hierarchy_list': hierarchy_list,
                                                       'baysianet': baysianet})


def hierarchy_new(request, baysianet_pk=None):
    context = {}
    if baysianet_pk:
        baysianet = get_object_or_404(BaysianNet, pk=baysianet_pk)
        context['baysianet'] = baysianet

    if request.method == "POST":
        form = HierarchyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('net_detail', baysianet_pk)
    else:
        form = HierarchyForm()

    return render(request, 'net/hierarchy_new.html', {'form': form,
                                                      'baysianet': baysianet})


def variable_detail(request, competency_pk=None):
    context = {}
    competence = get_object_or_404(Competence, pk=competency_pk)
    context['competence'] = competence
    return render(request, 'competence_detail.html', context)


@login_required
def variable_new(request, competency_pk=None, baysianet_pk=None):
    comp = get_object_or_404(Competence, pk=competency_pk)
    if request.method == "POST":
        form = VariableForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('net_detail', baysianet_pk)
    else:
        form = VariableForm()

    return render(request, 'net/variable_new.html', {'form': form, 'context': comp})


def ctp_new(request, competency_pk=None, baysianet_pk=None):
    ctp_dic_data = {}
    variable_dic_data = {}
    number = 1
    baysianet = get_object_or_404(BaysianNet, pk=baysianet_pk)
    hierarchies = Hierarchy.objects.filter(baysianet=baysianet_pk, competency_father=competency_pk)
    form = ConditionalProbabilityTableForm()
    for hierarchy in hierarchies:
        ctp_dic_data.update({hierarchy.competency_father: hierarchy.competency_father.variable.all()})
        variable_dic_data.update({hierarchy.competency_child: hierarchy.competency_child.variable.all()})
        number = number * hierarchy.competency_child.variable.all().count()

    return render(request, 'net/ctp_new.html', {'form': form,
                                                'ctp_dic_data': ctp_dic_data,
                                                'variable_dic_data': variable_dic_data,
                                                'range': range(number),
                                                'baysianet': baysianet,
                                                'competency_father': competency_pk})


def ctp_detail(request, competency_pk=None, baysianet_pk=None):
    context = {}
    baysianet = get_object_or_404(BaysianNet, pk=baysianet_pk)
    competency_father = ConditionalProbabilityTable.objects.filter(competency_father=competency_pk)
    context = {'baysianet': baysianet}
    return render(request, 'net/ctp_detail.html', {'baysianet': baysianet_pk,
                                                   'competency_father': competency_pk})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['username'],
                                            password=form.cleaned_data['password1'],
                                            email=form.cleaned_data['email'])
            return HttpResponseRedirect('/')
    form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)


def games(request):
    context = {}
    context['games'] = Game.objects.all()
    return render(request, 'game/index.html', context)


def play(request):
    context = {}
    context['games'] = Game.objects.all()
    return render(request, 'game/index.html', context)


def relatorios(request, game_pk=None):
    context = {}
    users = User.objects.all()
    user_dic_data = {}

    for user in users:
        total_correct = 0
        total_wrongs = 0
        for game_session in user.game_session.filter(game_id=game_pk):
            total_correct += game_session.log_session.filter(type_log=3).count()
            total_wrongs += game_session.log_session.filter(type_log=4).count()

        if total_correct != 0:
            user_dic_data[user.username] = {'accept': total_correct, 'wrong': total_wrongs, 'id': user.id}

    print(user_dic_data)
    wrong_dic_data = {}
    logs = LogSession.objects.filter(game_id=game_pk).filter(type_log=4)
    for wrongs in logs:
        if wrongs.expected in wrong_dic_data:
            wrong_dic_data[wrongs.expected]['value'] += 1
        else:
            wrong_dic_data[wrongs.expected] = {'value': 1}

    context['user_dic_data'] = user_dic_data
    context['wrong_dic_data'] = wrong_dic_data
    context['game'] = get_object_or_404(Game, pk=game_pk)
    return render(request, 'relatorios/index.html', context)


def relatorio_individual(request, user_pk=None, game_pk=None):
    context = {}
    wrong_dic_data = {}
    user_dic_data = {}
    game_session_dic_data = {}
    competence_dic_data = {}
    total_correct = 0
    total_wrongs = 0
    user = get_object_or_404(User, pk=user_pk)
    game_session = GameSession.objects.filter(game_id=game_pk).filter(user_id=user_pk)
    game = Game.objects.get(pk=game_pk)

    #Calculating percent for each competences of a game
    competences = Competence.objects.filter(game=game_pk)
    user_ctp_table_dic = {}
    for comp in competences:
        variable_dic = {}
        acerto = LogSession.objects.filter(user_id=user_pk).filter(competency=comp).filter(type_log=3).count()
        erro = LogSession.objects.filter(user_id=user_pk).filter(competency=comp).filter(type_log=4).count()
        total = acerto * 100 / (acerto + erro)
        competence_dic_data[comp.title] = {'name': comp.title}
        user_ctp_table_dic[comp.pk] = {'name': comp.title}
        variable = Variable.objects.filter(competence=comp)
        for var in variable:
            if var.title == "Alta":
                variable_dic.update({var.title: total})
            elif var.title == "Baixa":
                total_erro = erro * 100 / (acerto + erro)
                variable_dic.update({var.title: total_erro})
            else:
                variable_dic.update({var.title: 0})
        user_ctp_table_dic[comp.pk].update({'variable': variable_dic})
        competence_dic_data[comp.title].update({'variable': variable_dic})
        competence_dic_data[comp.title].update({'total': total})

    # Calculating percent for each logsession of a game
    for session in game_session:
        logs = LogSession.objects.filter(session=session.id)
        for log in logs:
            if log.type_log.value == 3:
                total_correct += 1
            elif log.type_log.value == 4:
                total_wrongs += 1
                if log.expected in wrong_dic_data:
                    wrong_dic_data[log.expected]['value'] += 1
                else:
                    wrong_dic_data[log.expected] = {'value': 1}

        game_session_dic_data[session.id] = {'game_session': session, 'accept': total_correct, 'wrong': total_wrongs,
                                             'id': user.id, 'percent_finish': session.percent_finish}

    # Calculate ctp father
    variables = {}
    var_child = list()
    lista = list()
    hierarquias_father = Hierarchy.objects.filter(competency_father_id=8).distinct('competency_father')
    for hierarq in hierarquias_father:
        hierarq_child = Hierarchy.objects.filter(competency_father_id=hierarq.competency_father_id)
        variable_father = Variable.objects.filter(competence=hierarq.competency_father_id)
        #variables.update({hierarq.competency_father: variable_father})

        for compe in hierarq_child:
            variable_child = Variable.objects.filter(competence=compe.competency_child_id)
            variables.update({compe.competency_child: variable_child})
            var_child.append(variable_child)


    lista = list(product(*variables.values()))



    for father in variable_father:
        for variables in lista:
            my_filter = list()
            palavra = ""
            query = Q()
            for var in variables:
                palavra += str(var.id) + " " + var.title + " "
                query |= Q(variable_child_id=var.id)
                #my_filter.append({'variable_child_id': var.id})


            ctps = ConditionalProbabilityTable.objects.filter(variable_father_id=father.pk)\
                  .filter(query)\
                  .values('line').annotate(Count('line')).order_by().filter(line__count__gt=1)

            print("Pai: {} {} Filho: {} Value: {}".format(father.id, father, palavra, ctps))

        #     for var in variables:
        #         query += var.title + " "
        #     print("Pai: {} Filho: {}".format(father, query))
        # query = ''
        #print("Pai: {} Filho: {}".format(father, query))

    #



    # SELECT * from core_conditionalprobabilitytable
    # WHERE variable_father_id = 19 AND (variable_child_id = 13 OR variable_child_id = 16) AND line in (
    #     SELECT line FROM core_conditionalprobabilitytable
    #     WHERE variable_father_id = 19 AND (variable_child_id = 13 OR variable_child_id = 16)
    #     group by line having count(*) > 1
    # )
    # ctps = ConditionalProbabilityTable.objects.filter(variable_father_id=19)\
    #     .filter(Q(variable_child_id=13) | Q(variable_child_id=16))\
    #     .values('line').annotate(Count('line')).order_by().filter(line__count__gt=1)
    #
    # for ctp in ctps:
    #     print(ctp)
        #print("{} {} {} ".format(ctp.variable_father, ctp.variable_child, ctp.value))

    #for variables in lista:
        #calcCTP(variables)
        #for var in variables:
            #print("{} {} {} ".format(var.pk,var.competence.title, var.title))
    #print(list[1].variable)
    #for father in hierarq.

    #print(hierarquias_father)
    user_dic_data[user.username] = {'accept': total_correct, 'wrong': total_wrongs, 'id': user.id}
    #print(user_ctp_table_dic)
    #save informacion in context
    context['game_session_dic_data'] = game_session_dic_data
    context['wrong_dic_data'] = wrong_dic_data
    context['user_dic_data'] = user_dic_data
    context['game'] = game
    context['competence_dic_data'] = competence_dic_data
    context['userRelatorio'] = user
    return render(request, 'relatorios/individual.html', context)

def calcCTP(variable):
    print(variable)

def simulator(request, session_pk=None):
    context = {}
    logs = LogSession.objects.filter(session_id=session_pk)
    session = GameSession.objects.get(pk=session_pk)
    context['game'] = get_object_or_404(Game, pk=session.game_id)
    context['logs'] = logs
    return render(request, 'relatorios/simulator.html', context)
