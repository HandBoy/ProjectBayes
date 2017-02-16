from django.shortcuts import render, redirect, get_object_or_404
from core.models import BaysianNet, Competence, Hierarchy, HierarchyFather
from core.forms import BaysianForm, CompetenceForm, VariableForm


# Create your views here.
def index(request):
    context = {}
    context['nets'] = BaysianNet.objects.all()
    # Number of visits to this view, as counted in the session variable.
    num_visits=request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1
    context['num_visits'] = num_visits
    return render(request, 'index.html', context)



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
    baysianet = get_object_or_404(BaysianNet, pk=pk)
    context['baysianet'] = baysianet
    return render(request, 'baysianet_detail.html', context)


def competencies(request):
    context = {}
    context['competencia'] = Competence.objects.all()
    return render(request, 'competencies.html', context)

def competence_detail(request, pk):
    context = {}
    competence = get_object_or_404(Competence, pk=pk)
    context['competence'] = competence
    return render(request, 'baysianet_detail.html', context)

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
            return redirect('core.views.baysianet_detail', baysianet_pk)
    else:
        form = CompetenceForm()
    return render(request, 'competence_new.html', {'form': form,
                                                   'hierarchy_list': hierarchy_list,
                                                   'baysianet': baysianet})

def variable_detail(request, competency_pk=None):
    context = {}
    competence = get_object_or_404(Competence, pk=pk)
    context['competence'] = competence
    return render(request, 'competence_detail.html', context)

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
