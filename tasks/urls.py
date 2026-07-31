from django.urls import path
from . import views

urlpatterns=[
    path("", views.task_list, name="task_list"),
    path("create/", views.create_task, name="create_task"),
    path("<int:id>/", views.task_detail, name="task_detail"),
    path("<int:id>/edit/", views.task_update, name="task_update"),
    path("<int:id>/delete/", views.task_delete, name="task_delete"),
    # Nouvelle route : bascule coché/décoché en AJAX
    path("<int:id>/toggle/", views.task_toggle, name="task_toggle"),
]