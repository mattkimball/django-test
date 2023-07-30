from django.urls import path
from . import views


app_name = 'todo'

urlpatterns = [
    path('', views.home, name='home'),
    path('task-list', views.TaskListView.as_view(), name='task-list'),
    path('add-task', views.task_create, name='task-create'),
    path('tasks/<int:id>/toggle', views.task_toggle, name='task-toggle'),
    path('tasks/clear-completed', views.clear_completed_tasks, name='clear-completed'),
]