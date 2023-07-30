from django.http import HttpResponse
from django.shortcuts import render, redirect
from typing import Any, Dict
from django.views.generic import ListView, CreateView
from todo.models import Task
from todo.forms import TaskForm


def home(request):
    tasks = Task.objects.all().order_by('id').reverse()
    form = TaskForm()
    context = {'tasks': tasks, 'form': form}
    return render(request, 'todo/home.html', context)


class TaskListView(ListView):
    model = Task
    template_name = 'todo/task-list.html'
    context_object_name = 'tasks'


def task_create_view(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        form.save()
    tasks = Task.objects.all().order_by('id').reverse()
    form = TaskForm()
    context = {'tasks': tasks, 'form': form}
    return render(request, 'todo/task-list.html', context)


def task_toggle(request, id):
    task = Task.objects.get(id=id)
    task.complete = not task.complete
    task.save()
    return HttpResponse('Success')