from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from todo.models import Task
from todo.forms import TaskForm


@login_required
def home(request):
    tasks = Task.objects.all().order_by("id").reverse()
    form = TaskForm()
    context = {"tasks": tasks, "form": form}
    return render(request, "todo/home.html", context)


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "todo/task-list.html"
    context_object_name = "tasks"
    ordering = ["-id"]

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["form"] = TaskForm()
        return context


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect(reverse("todo:task-list"))


@login_required
def task_list_item(request, id):
    task = Task.objects.get(id=id)
    return render(request, "todo/task-list-item.html", {"task": task})


@login_required
def task_toggle(request, id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        task.complete = not task.complete
        task.save()
    return redirect(reverse("todo:task-list-item", args=(task.id,)))


@login_required
def task_edit(request, id):
    task = Task.objects.get(id=id)
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task.name = form.cleaned_data["name"]
            task.save()
        else:
            pass
        return redirect(reverse("todo:task-list-item", args=(task.id,)))
    else:
        form = TaskForm(instance=task)
        form.fields["name"].label = "Task"
        context = {
            "form": form,
            "task": task,
        }
        return render(request, "todo/task-edit.html", context)


@login_required
def task_delete(request, id):
    if request.method == "POST":
        task = Task.objects.get(id=id)
        task.delete()

    return HttpResponse("")


@login_required
def clear_completed_tasks(request):
    if request.method == "POST":
        tasks = Task.objects.filter(complete=True)
        for task in tasks:
            task.delete()

    return redirect(reverse("todo:task-list"))
