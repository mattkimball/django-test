from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView

from django_htmx.http import HttpResponseClientRefresh

from tasks.models import Task
from tasks.forms import TaskForm


class TaskListView(LoginRequiredMixin, ListView):
    queryset = Task.objects.filter(archived=False).order_by('-id')
    template_name = "tasks/task-list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()
        return context


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            return render(request, 'tasks/task-list.html#task-list-item', {'task': task})


@login_required
def task_item(request, id):
    task = Task.objects.get(id=id)
    return render(request, 'tasks/task-list.html#task-list-item', {'task': task})


@login_required
def task_toggle(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        if task.complete:
            task.complete = False
            task.completed_at = None
        else:
            task.complete = True
            task.completed_at = timezone.now()
        task.save()
        return render(request, 'tasks/task-list.html#task-list-item', {'task': task})


@login_required
def task_edit(request, id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task.name = form.cleaned_data["name"]
            task.save()
        return render(request, 'tasks/task-list.html#task-list-item', {'task': task})
    else:
        form = TaskForm(instance=task)
        form.fields["name"].label = "Task"
        context = {
            "form": form,
            "task": task,
        }
        return render(request, 'tasks/task-list.html#task-list-item-edit', context)


@login_required
def task_delete(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()

    return HttpResponse("")


@login_required
def clear_completed(request):
    if request.method == "POST":
        tasks = Task.objects.filter(complete=True)
        for task in tasks:
            task.archived = True
            task.save()
    
    return HttpResponseClientRefresh()
