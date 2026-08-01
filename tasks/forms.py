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
        fields = ["title", "description", "due_date"]

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Ex. Réviser la théorie des langages",
            }),
            "description": forms.Textarea(attrs={
                "class": "form-textarea",
                "placeholder": "Détails de la tâche...",
                "rows": 4,
            }),
            "due_date": forms.DateInput(
                attrs={"class": "form-input", "type": "date"},
                format="%Y-%m-%d",  # format d'AFFICHAGE (préremplissage du champ)
            ),
        }

        # On personnalise les libellés affichés (sinon Django utilise
        # automatiquement "Title", "Description", "Due date")
        labels = {
            "title": "Titre",
            "description": "Description",
            "due_date": "Date d'échéance",
        }

    def __init__(self, *args, **kwargs):
        # Cette fonction se déclenche automatiquement à chaque création du formulaire.

        # On garde d'abord tout le comportement normal de ModelForm
        # (sinon self.fields n'existerait pas encore, et la ligne suivante planterait)
        super().__init__(*args, **kwargs)

        # Puis on ajoute notre réglage : on dit à Django d'accepter le format
        # AAAA-MM-JJ quand l'utilisateur soumet la date, car c'est TOUJOURS
        # ce format que le navigateur envoie pour un champ type="date"
        self.fields["due_date"].input_formats = ["%Y-%m-%d"]