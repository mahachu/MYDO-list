from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_POST
# Create your views here.

def task_list(request):
    """
    Vue principale de la page des tâches.
    Elle sert deux usages avec UNE SEULE fonction :
      1) Affichage classique de la page complète (première visite, F5...)
      2) Réponse "légère" en JSON quand elle est appelée par le JavaScript
         (recherche, changement de filtre), sans recharger toute la page.
    """
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")  # "", "todo" ou "completed"
 
    # Base commune : toutes les tâches qui correspondent à la recherche
    # (avant d'appliquer le filtre de statut). Sert à calculer les 3 compteurs.
    base = Task.objects.all()
    if search:
        base = base.filter(Q(title__icontains=search) | Q(description__icontains=search))
 
    all_count = base.count()
    todo_count = base.filter(completed=False).count()
    completed_count = base.filter(completed=True).count()
 
    # Application du filtre de statut, en plus de la recherche, pour la liste affichée
    tasks = base
    if status == "todo":
        tasks = tasks.filter(completed=False)
    elif status == "completed":
        tasks = tasks.filter(completed=True)
 
    context = {
        "tasks": tasks,
        "search": search,
        "status": status,
        "all_count": all_count,
        "todo_count": todo_count,
        "completed_count": completed_count,
    }

    # Requête AJAX (envoyée par script.js) : on ne renvoie que le fragment HTML de la liste + le compteur 
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            "tasks/_task_list_partial.html",
            {"tasks": tasks, "search": search},
            request=request,
        )
        return JsonResponse({
            "html": html,
            "all_count": all_count,
            "todo_count": todo_count,
            "completed_count": completed_count,
        })
    # Chargement classique de la page (première visite, F5, lien direct...)
    return render(request, "tasks/task_list.html", context)



@require_POST  # on n'autorise que le POST : on ne veut pas qu'un simple GET modifie la BDD
def task_toggle(request, id):
    
    """
    Bascule l'état 'completed' d'une tâche (appelée en AJAX quand on
    (dé)coche la case dans la liste).
    - Si on coche  -> completed = True  + completed_date = aujourd'hui
    - Si on décoche -> completed = False + completed_date = None
    Renvoie un JSON, car cette vue n'est appelée qu'en AJAX (jamais en navigation classique).
    """
    task = get_object_or_404(Task, id=id)

    # On inverse simplement l'état actuel
    task.completed = not task.completed
    task.completed_date = timezone.localdate() if task.completed else None
    task.save()

    return JsonResponse({
        "success": True,
        "completed": task.completed,
        "status": task.status,  # utile si un jour tu veux mettre à jour le badge sans tout recharger
    })

def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request, "tasks/task_form.html", {"form":form})

def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    return render (request, "tasks/task_detail.html", {"task":task})

def task_update(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance = task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm( instance = task)
    return render(request, "tasks/task_form.html", {"form": form})

def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        task.delete()
        return redirect("task_list")
    return render(request, "tasks/task_confirm_delete.html",{"task":task})