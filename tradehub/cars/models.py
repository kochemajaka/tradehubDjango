from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
class KanbanCols(models.Model):
    name = models.CharField(unique=True)
    stage = models.CharField(max_length=20)
    cross = models.ForeignKey('self', on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'kanban'

class Wheels(models.Model):
    diskType = models.CharField(max_length=30)
    season = models.CharField(max_length=30)
    tireWidth = models.IntegerField()
    tireHeight = models.IntegerField()
    tireDiameter = models.IntegerField()
    tireManufacture = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    class Meta:
        db_table = 'wheel'
class Cars(models.Model):
    stageId = models.ForeignKey(to=KanbanCols, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=100, null=True, blank=True)
    brand = models.CharField(max_length=35)
    model = models.CharField(max_length=35)
    VIN = models.CharField(max_length=17, unique=True, null=True, blank=True)
    year = models.IntegerField()
    odometer = models.IntegerField(null=True, blank=True)
    engine = models.CharField(max_length=20, null=True, blank=True)
    transmission = models.CharField(max_length=20, null=True, blank=True)
    photo = models.ImageField(upload_to="", null=True, blank=True, default='default.png')

    def save(self, *args, **kwargs):
        # Проверка на существование объекта и изменение stageId
        if self.pk:
            original = Cars.objects.get(pk=self.pk)
            if original.stageId != self.stageId:
                # Создание записи в KanbanDates при изменении stageId
                KanbanDates.objects.create(
                    stadeId=self.stageId,
                    carId=self,
                    transferDate=datetime.today()
                )
        # Вызов родительского метода save
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'car'

class Employees(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    fatherName = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    mail = models.EmailField()
    position = models.CharField(max_length=30)
    status = models.CharField(max_length=40, null=True, blank=True)
    dateBirdth = models.DateField(null=True, blank=True)
    department = models.CharField(max_length=20)

    def full_name(self):
        return f"{self.lastName} {self.name} {self.fatherName}"

    class Meta:
        db_table = 'employee'

class Entities(models.Model):
    passportNumber = models.CharField(max_length=10)
    dateBirdth = models.DateField()
    dateIssue = models.DateField()
    code = models.CharField(max_length=7)
    institution = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    fatherName = models.CharField(max_length=20)
    place = models.CharField(max_length=30)
    registration = models.CharField(max_length=255)

    def full_name(self):
        return f"{self.lastName} {self.name} {self.fatherName}"

    class Meta:
        db_table = 'entity'

class PrebuyCars(models.Model):
    carId = models.OneToOneField(to=Cars, on_delete=models.DO_NOTHING)
    employeeId = models.ForeignKey(to=Employees, on_delete=models.DO_NOTHING)
    prebuyDate = models.DateField()
    rank = models.IntegerField(null=True, blank=True)
    typeSourse = models.CharField(max_length=30,null=True, blank=True)
    carSourse = models.CharField(max_length=30,null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    prepositionNote = models.TextField(null=True, blank=True)
    carCost = models.IntegerField()
    marginality = models.FloatField()
    predictCost = models.IntegerField()
    liquidRatio = models.FloatField(null=True, blank=True)


    class Meta:
        db_table = 'prebuy_car'

class DDS(models.Model):
    carId = models.ForeignKey(to=Cars, on_delete=models.DO_NOTHING, null=True, blank=True)
    employeeId = models.ForeignKey(to=Employees, on_delete=models.DO_NOTHING)
    article = models.CharField(max_length=100)
    operationDate = models.DateField()
    amount = models.FloatField()
    paymentAccount = models.CharField(max_length=30)
    description = models.CharField(max_length=255, null=True, blank=True)
    isProfit = models.BooleanField()

    class Meta:
        db_table = 'dds'

class BuyCars(models.Model):
    carId = models.OneToOneField(to=Cars, on_delete=models.DO_NOTHING)
    entityId = models.ForeignKey(to=Entities, on_delete=models.DO_NOTHING)
    ddsId = models.ForeignKey(to=DDS, on_delete=models.DO_NOTHING)
    # tire = models.ForeignKey(to=Wheels, on_delete=models.DO_NOTHING)
    owners = models.IntegerField(null=True, blank=True)
    govNum = models.CharField(max_length=9, null=True, blank=True)
    typePTS = models.CharField(max_length=20, null=True, blank=True)
    cntKeys = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'buy_car'


class Tasks(models.Model):
    carId = models.ForeignKey(to=Cars, on_delete=models.DO_NOTHING)
    employeeId = models.ForeignKey(to=Employees, on_delete=models.DO_NOTHING)
    stageId = models.ForeignKey(to=KanbanCols, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    priority = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30)
    taskDate = models.DateField()
    completeDate = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'task'

class Diagnostics(models.Model):
    carId = models.ForeignKey(to=Cars, on_delete=models.DO_NOTHING)
    employeeId = models.ForeignKey(to=Employees, on_delete=models.DO_NOTHING)
    diagnosticDate = models.DateField()
    odometer = models.IntegerField(null=True, blank=True)
    engine = models.CharField(max_length=255, null=True, blank=True)
    transmission = models.CharField(max_length=255, null=True, blank=True)
    suspension = models.CharField(max_length=255, null=True, blank=True)
    tires = models.CharField(max_length=255, null=True, blank=True)
    steering = models.CharField(max_length=255, null=True, blank=True)
    brake = models.CharField(max_length=255, null=True, blank=True)
    electrical = models.CharField(max_length=255, null=True, blank=True)
    climate = models.CharField(max_length=255, null=True, blank=True)
    dasboard = models.CharField(max_length=255, null=True, blank=True)
    diagnostics = models.TextField(null=True, blank=True)
    windshield = models.CharField(max_length=255, null=True, blank=True)
    PZD = models.IntegerField(null=True, blank=True)
    PPD = models.IntegerField(null=True, blank=True)
    PPK = models.IntegerField(null=True, blank=True)
    PZK = models.IntegerField(null=True, blank=True)
    PB = models.IntegerField(null=True, blank=True)
    ZB = models.IntegerField(null=True, blank=True)
    KAP = models.IntegerField(null=True, blank=True)
    KRH = models.IntegerField(null=True, blank=True)
    KB = models.IntegerField(null=True, blank=True)
    LZK = models.IntegerField(null=True, blank=True)
    LPK = models.IntegerField(null=True, blank=True)
    LZD = models.IntegerField(null=True, blank=True)
    LPD = models.IntegerField(null=True, blank=True)
    factoryLKP = models.IntegerField(null=True, blank=True)
    descriptionLKP = models.CharField(max_length=255, null=True, blank=True)
    testdrive = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField()
    autoteka = models.URLField()

    class Meta:
        db_table = 'diagnostic'

class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'brand'

class Model(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'models'

class BrandModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='brands')

    class Meta:
        db_table = 'brand_model'
        unique_together = ('brand', 'model')  # Ограничение уникальности для предотвращения дубликатов

class MoneyArticles(models.Model):
    name = models.CharField(max_length=255, unique=True)
    isProfit = models.BooleanField()

    class Meta:
        db_table = 'money_article'

class CarSources(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'car_source'

class ClientSources(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'client_source'

class DDSAccounts(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'dds_account'

class Widgets(models.Model):
    departmentName = models.CharField(max_length=100)
    positionName = models.CharField(max_length=100)
    widgetName = models.CharField(max_length=100)

    class Meta:
        db_table = 'widget'

class EmployeeWidgets(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    widget = models.ManyToManyField(Widgets)


class Meta:
    db_table = 'employee_widget'

class KanbanDates(models.Model):
    stadeId = models.ForeignKey(KanbanCols, on_delete=models.CASCADE)
    carId = models.ForeignKey(Cars, on_delete=models.CASCADE)
    transferDate = models.DateField()

    class Meta:
        db_table = 'kanban_date'