from cars.models import Cars,PrebuyCars
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, Form
from django.db import models

class AuthUserForm(AuthenticationForm, ModelForm):
    class Meta:
        model = User
        fields = ("username","password")

from .models import PrebuyCars, Cars, Employees  # Импортируйте необходимые модели

class CarForm(ModelForm):
    class Meta:
        model = Cars
        fields = [
            'brand',
            'model',
            'VIN',
            'year',
            'engine',
            'transmission',
            'odometer',
        ]

class PrebuyCarForm(ModelForm):
    class Meta:
        model = PrebuyCars
        fields = [
            'employeeId',
            'rank',
            'typeSourse',
            'carSourse',
            'description',
            'prepositionNote',
            'carCost',
            'marginality',
            'predictCost',
            'liquidRatio'
        ]

class AddEmployeeForm(Form):
    firstname = models.CharField(max_length=20, name="firstname")
    lastName = models.CharField(max_length=20)
    fatherName = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    mail = models.EmailField()
    department = models.CharField(max_length=20)
    position = models.CharField(max_length=30)
    datebirdth = models.DateField(null=True, blank=True)
    password1 = models.CharField(max_length=20)
    password2 = models.CharField(max_length=20)