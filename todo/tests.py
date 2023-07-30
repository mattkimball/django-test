from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from todo.models import Task
from todo.forms import TaskForm


class TaskTestCase(TestCase):
    
    def setUp(self):
        self.task = Task.objects.create(name='Test Task')
    
    
    def test_task_name(self):
        self.assertEqual(self.task.name, 'Test Task')
    
    
    def test_task_complete(self):
        self.assertFalse(self.task.complete)
    
    
    def test_task_str_representation(self):
        self.assertEqual(str(self.task), 'Test Task')


class TaskFormTestCase(TestCase):
    
    def test_task_form_valid_data(self):
        form_data = {'name': 'Test Task'}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    
    def test_task_form_cleaned_data(self):
        form_data = {'name': '  Test Task  '}
        form = TaskForm(data=form_data)
        form.full_clean()
        self.assertEqual(form.cleaned_data['name'], 'Test Task')
    
    
    def test_task_form_invalid_data(self):
        form_data = {'name': ''}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())


class TaskViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(name='Test Task')
        
        self.home_url = reverse('todo:home')
        self.task_list_url = reverse('todo:task-list')
        self.task_create_url = reverse('todo:task-create')
        self.task_toggle_url = reverse('todo:task-toggle', args=(self.task.id,))
        self.clear_completed_url = reverse('todo:clear-completed')
    
    
    def test_home_get(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('todo/home.html')
    
    
    def test_task_list_get(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('todo/task-list.html')
    
    
    def test_task_create_post(self):
        post_data = {'name': 'Test Task'}
        response = self.client.post(self.task_create_url, post_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)
    
    
    def test_task_toggle_post(self):
        response = self.client.post(self.task_toggle_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('todo/task-list-item.html')
    
    
    def test_clear_completed_post(self):
        response = self.client.post(self.clear_completed_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.task_list_url)