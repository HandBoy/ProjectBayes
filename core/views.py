from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.template import RequestContext

from core.models import BaysianNet, Competence, LogSession, Game, GameSession, CompetenceUser, Hierarchy
from core.forms import BaysianForm, CompetenceForm, VariableForm, RegistrationForm, HierarchyForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Create your views here.
def index(request):
    context = {}
    context['nets'] = BaysianNet.objects.all()
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
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
    print(father.count())
    for pai in father.all():
        print(pai.competency_father_id)
        filhos = hierarchies.filter(competency_father=pai.competency_father_id)
        print(filhos.count())
        rede[pai.competency_father] = filhos.all()
        #for filho in filhos.all():
            #rede[pai.competency_father].append(filho)

    print(rede)
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
def variable_new(request, competency_pk=None):
    comp = get_object_or_404(Competence, pk=competency_pk)
    if request.method == "POST":
        form = VariableForm(request.POST)
        if form.is_valid():
            form.save()
            return render('core.views.baysianet_detail.html', pk=comp.baysianet_id)
    else:
        form = VariableForm()

    return render(request, 'variable_new.html', {'form': form, 'context': comp})


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
    return render_to_response('registration/register.html',variables)


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
            total_wrongs   += game_session.log_session.filter(type_log=4).count()

        if total_correct != 0:
            user_dic_data[user.username] = {'accept': total_correct, 'wrong': total_wrongs, 'id': user.id}

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

    #
    competences = Competence.objects.filter(game=game_pk)
    for comp in competences:
        acerto = LogSession.objects.filter(user_id=user_pk).filter(competency=comp).filter(type_log=3).count()
        erro = LogSession.objects.filter(user_id=user_pk).filter(competency=comp).filter(type_log=4).count()
        total = acerto*100/(acerto+erro)
        competence_dic_data[comp.title] = {'name': comp.title}
        competence_dic_data[comp.title] = {'acerto': acerto}
        competence_dic_data[comp.title] = {'erro': erro}
        competence_dic_data[comp.title] = {'total': total}


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

    user_dic_data[user.username] = {'accept': total_correct, 'wrong': total_wrongs, 'id': user.id}
    context['game_session_dic_data'] = game_session_dic_data
    context['wrong_dic_data'] = wrong_dic_data
    context['user_dic_data'] = user_dic_data
    context['game'] = game
    context['competence_dic_data'] = competence_dic_data
    context['userRelatorio'] = user
    return render(request, 'relatorios/individual.html', context)


def simulator(request, session_pk=None):
    context = {}
    logs = LogSession.objects.filter(session_id=session_pk)
    session = GameSession.objects.get(pk=session_pk)
    context['game'] = get_object_or_404(Game, pk=session.game_id)
    context['logs'] = logs
    return render(request, 'relatorios/simulator.html', context)