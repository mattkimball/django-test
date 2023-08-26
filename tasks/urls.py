from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="list"),
    path("tasks/add", views.task_create, name="create"),
    path("tasks/<int:id>", views.task_item, name="item"),
    path("tasks/<int:id>/toggle", views.task_toggle, name="toggle"),
    path("tasks/<int:id>/edit", views.task_edit, name="edit"),
    path("tasks/<int:id>/delete", views.task_delete, name="delete"),
    path("tasks/clear-completed", views.clear_completed, name="clear-completed"),
]