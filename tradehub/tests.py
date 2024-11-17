from django.test import TestCase
from cars.models import Cars, Tasks
from django.urls import reverse

class CarModelTest(TestCase):
    def setUp(self):
        self.car = Cars.objects.create(name="Test Car", model="Test Model")

    def test_car_creation(self):
        car = Cars.objects.get(name="Test Car")
        self.assertEqual(car.model, "Test Model")
        self.assertTrue(isinstance(car, Cars))

class TaskViewTest(TestCase):
    def setUp(self):
        self.task = Tasks.objects.create(name="Test Task", status="active")

    def test_task_list_view(self):
        response = self.client.get(reverse("task_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "yourapp/task_list.html")

class TaskStatusUpdateTest(TestCase):
    def setUp(self):
        self.task = Tasks.objects.create(name="Test Task", status="active")

    def test_complete_task(self):
        response = self.client.post(f"/kanban/tasks/complete/", {"taskIds": [self.task.id]})
        self.assertEqual(response.status_code, 200)

        # Обновление объекта задачи из базы данных
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "complete")
