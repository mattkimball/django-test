from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from tasks.models import Task
from tasks.forms import TaskForm


class TaskTestCase(TestCase):
    
    def setUp(self):
        self.task = Task.objects.create(name="Test Task")


    def test_task_name(self):
        self.assertEqual(self.task.name, "Test Task")


    def test_task_complete(self):
        self.assertFalse(self.task.complete)


    def test_task_str_representation(self):
        self.assertEqual(str(self.task), "Test Task")


class TaskFormTestCase(TestCase):

    def test_task_form_valid_data(self):
        form_data = {"name": "Test Task"}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())


    def test_task_form_cleaned_data(self):
        form_data = {"name": "  Test Task  "}
        form = TaskForm(data=form_data)
        form.full_clean()
        self.assertEqual(form.cleaned_data["name"], "Test Task")


    def test_task_form_invalid_data(self):
        form_data = {"name": ""}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())


class TaskViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(username="testuser")
        self.client.force_login(self.user)
        
        self.task = Task.objects.create(name="Test Task")

        self.task_list_url = reverse("tasks:list")
        self.task_item_url = reverse("tasks:item", args=(self.task.id,))
        self.task_create_url = reverse("tasks:create")
        self.task_toggle_url = reverse("tasks:toggle", args=(self.task.id,))
        self.task_edit_url = reverse("tasks:edit", args=(self.task.id,))
        self.task_delete_url = reverse("tasks:delete", args=(self.task.id,))
        self.clear_completed_url = reverse("tasks:clear-completed")


    def test_task_list_get(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("tasks/task-list.html")


    def test_task_create_post(self):
        post_data = {"name": "Test Task"}
        response = self.client.post(self.task_create_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("tasks/task-list.html#task-list-item")
    
    
    def test_task_list_item_get(self):
        response = self.client.get(self.task_item_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("tasks/task-list.html#task-list-item")
    
    
    def test_task_toggle_post(self):
        response = self.client.post(self.task_toggle_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('tasks/task-list.html#task-list-item')
    

    def test_task_edit_get(self):
        response = self.client.get(self.task_edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("tasks/task-list.html#task-list-item-edit")


    def test_task_edit_post(self):
        post_data = {"name": "Test Tasi"}
        response = self.client.post(self.task_edit_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("tasks/task-list.html#task-list-item")


    def test_task_delete_post(self):
        response = self.client.post(self.task_delete_url)
        self.assertEqual(response.status_code, 200)


    def test_clear_completed_post(self):
        response = self.client.post(self.clear_completed_url)
        self.assertEqual(response.status_code, 200)
