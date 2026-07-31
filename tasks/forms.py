from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    Formulaire de création/modification d'une tâche.
    Les 'widgets' ci-dessous servent à ajouter des attributs HTML
    (classe CSS, placeholder...) directement sur les champs générés
    par Django, pour pouvoir les styliser dans style.css.
    """

    class Meta:
        model = Task
        fields = ["title", "description", "due_date",]

        widgets = { "title": forms.TextInput(attrs={"class":"form-input", "placeholder":"Ex. Réviser la théorie des langages", }),
               "description":forms.Textarea(attrs={"class":"form-textarea", "placeholder":"Détails de la tâche...", "rows": 4, }),
               "due_date":forms.DateInput(attrs={"class":"form-input", "type":"date", }),
        }

        labels = {
        # On personnalise les libellés affichés (sinon Django utilise
        # automatiquement "Title", "Description", "Due date")
        "title": "Titre",
        "description": "Description",
        "due_date": "Date d'échéance",
        }