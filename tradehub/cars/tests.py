import json
from django.test import TestCase
from .models import Cars, Tasks, KanbanCols, Employees
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

class CarModelTest(TestCase):
    def setUp(self):
        self.kanban = KanbanCols(
            name = "Test stage",
        )
        self.kanban.save()

        self.car = Cars.objects.create(
            stageId = KanbanCols.objects.get(name="Test stage"),
            name = "Test Car",
            brand = "Test brand",
            model = "Test Model",
            VIN = "1230ldwka",
            year = 2021,
            odometer = 123000
        )
        self.car.save()

    def test_car_creation(self):
        car = Cars.objects.get(name="Test Car")
        self.assertEqual(car.model, "Test Model")
        self.assertTrue(isinstance(car, Cars))

class TaskTest(TestCase):
    def setUp(self):
        self.kanban = KanbanCols(
            name = "Test stage",
        )
        self.kanban.save()

        self.car = Cars.objects.create(
            stageId = KanbanCols.objects.get(name="Test stage"),
            name = "Test Car",
            brand = "Test brand",
            model = "Test Model",
            VIN = "1230ldwka",
            year = 2021,
            odometer = 123000
        )
        self.car.save()

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()

        # Создаем объект Employees
        self.employee = Employees.objects.create(
            user=self.user,
            name="John",
            lastName="Doe",
            fatherName="Smith",
            phone="1234567890",
            mail="john.doe@example.com",
            position="Manager",
            status="Active",
            dateBirdth="1980-01-01",
            department="Sales"
        )
        self.employee.save()

        # Создаем объект Tasks, связанный с Employees
        self.task = Tasks.objects.create(
            carId= self.car,
            employeeId = self.employee,
            stageId = self.kanban,
            name = "Tesk task",
            priority = 5,
            status = "Fctive",
            taskDate = date(2024, 10, 27)
        )
        self.task.save()

    def test_task_creation(self):
        task = Tasks.objects.get(name="Tesk task")
        self.assertEqual(task.status, "Fctive")
        self.assertTrue(isinstance(task, Tasks))

    def test_complete_task(self):
        response = self.client.post(
            f"/kanban/tasks/complete/",
            data=json.dumps({"carId": self.car.id, "taskIds": [self.task.id]}),
            content_type="application/json"
        )

        self.task.refresh_from_db()
        self.assertEqual(self.task.status, "complete")

class EndpointAccessTests(TestCase):
    # def setUp(self):
        # Создаем тестового пользователя
        # self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_access(self):
        response = self.client.get(reverse('login_page'))
        self.assertEqual(response.status_code, 200)  # Должен быть доступен без авторизации

    def test_logout_access(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Перенаправление на логин

    def test_home_access(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление на логин

    def test_settings_access(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 302)

    def test_form_access(self):
        response = self.client.get(reverse('form_page'))
        self.assertEqual(response.status_code, 302)

    def test_stock_access(self):
        response = self.client.get(reverse('sclad_page'))
        self.assertEqual(response.status_code, 302)

    def test_analytics_access(self):
        response = self.client.get(reverse('analytics'))
        self.assertEqual(response.status_code, 302)

    def test_kanban_access(self):
        response = self.client.get(reverse('kanban'))
        self.assertEqual(response.status_code, 302)
