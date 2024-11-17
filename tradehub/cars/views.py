from datetime import datetime, timedelta, date
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .models import *  # Импортируйте необходимые модели
from .forms import AddEmployeeForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from datetime import timedelta
import calendar
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

class TradehubLoginView(LoginView):
    template_name = "login.html"
    form_class = AuthUserForm
    success_url = reverse_lazy("home")


from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


# Декоратор для проверки позиции в модели Employees
def position_required(required_position):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                employee = request.user.employees.first()

                if employee and employee.position == required_position:
                    return view_func(request, *args, **kwargs)
                else:
                    # Если позиция не совпадает, перенаправляем на другую страницу или показываем ошибку
                    return redirect('login')  # Страница для тех, у кого нет доступа
            except Employees.DoesNotExist:
                # Если сотрудник не найден, перенаправляем на страницу без доступа
                return redirect('login')

        return _wrapped_view

    return decorator

@login_required
def KanbanPageView(request):
    columns = KanbanCols.objects.all()
    column_car_counts = {}
    for column in columns:
        column.cars = Cars.objects.filter(stageId=column)
        column_car_counts[column.id] = Cars.objects.filter(stageId=column).count()

    return render(request, 'kanban.html', {
        'columns': columns,
        'column_car_counts': column_car_counts,
    })

def GetTasks(request, car_id):
    if request.method == 'GET':
        try:
            carId = int(car_id)
            tasks = Tasks.objects.filter(carId_id=carId, status='active').values(
                'id', 'name', 'description', 'priority', 'status', 'deadline', 'taskDate'
            )
            task_list = list(tasks)  # Преобразуем QuerySet в список

            car = Cars.objects.get(id=carId)
            car_name = car.name

            response_data = {
                'car_name': car_name,
                'tasks': task_list
            }
            return JsonResponse(response_data, safe=False)  # Возвращаем данные в формате JSON

        except Cars.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Car not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Try repeat.'})

def CompleteTasks(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            task_ids = data.get('taskIds', [])

            # Обновляем статус задач
            Tasks.objects.filter(id__in=task_ids).update(status='complete')
            return JsonResponse({'status': 'success', 'message': 'Задачи успешно обновлены'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Неверный метод запроса'})
@csrf_exempt  # Убедитесь, что CSRF-токены обрабатываются правильно в вашем проекте
def UpdateStage(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        car_id = data.get('car_id')
        stage_id = data.get('stage_id')


        try:
            carId = int(car_id)
            car = Cars.objects.get(id=carId)
            car.stageId_id = stage_id  # Обновляем stageId
            car.save()

            return JsonResponse({'status': 'success'})
        except Cars.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Car not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': 'Try repeat.'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})
@login_required
@position_required('top')
def SettingsPageTop(request):
    employee = request.user.employees.first()

    if employee.dateBirdth and isinstance(employee.dateBirdth, str):
        try:
            # Преобразуем строку в объект datetime, если это строка
            date_birdth_obj = datetime.strptime(employee.dateBirdth, '%Y-%m-%d')
            dateBirdth = date_birdth_obj.strftime('%Y-%m-%d')
        except ValueError:
            # Обработка ошибки, если формат даты неверен
            dateBirdth = ''
    elif employee.dateBirdth:
        # Если это уже объект даты, то просто форматируем его
        dateBirdth = employee.dateBirdth.strftime('%Y-%m-%d')

    context = {
        'name': employee.name,
        'lastName': employee.lastName,
        "fatherName": employee.fatherName,
        "phone": employee.phone,
        "email": employee.mail,
        "dateBirdth":  dateBirdth,
        "active_tab": "1"
    }
    return render(request, "settings.html", context)

@login_required
@position_required('top')
def AddUserForm(request):
    employee = request.user.employees.first()

    if employee.dateBirdth and isinstance(employee.dateBirdth, str):
        try:
            # Преобразуем строку в объект datetime, если это строка
            date_birdth_obj = datetime.strptime(employee.dateBirdth, '%Y-%m-%d')
            dateBirdth = date_birdth_obj.strftime('%Y-%m-%d')
        except ValueError:
            # Обработка ошибки, если формат даты неверен
            dateBirdth = ''
    elif employee.dateBirdth:
        # Если это уже объект даты, то просто форматируем его
        dateBirdth = employee.dateBirdth.strftime('%Y-%m-%d')
    context = {
        'name': employee.name,
        'lastName': employee.lastName,
        "fatherName": employee.fatherName,
        "phone": employee.phone,
        "email": employee.mail,
        "dateBirdth": dateBirdth,
        "active_tab": "3"
    }

    if request.method == 'POST':
            data = request.POST

            if data['password1'] != data['password2']:
                message = "Пароли не совпадают!"
                context["message"] = message
                return render(request, "settings.html", context)
            try:
                if User.objects.filter(username=data['mail']).exists():
                    message = "Пользователь с таким email уже существует!"
                    context["message"] = message
                    return render(request, "settings.html", context)

                validate_password(data['password1'])
                usr = User(username=data['mail'])

                usr.set_password(data['password1'])
                usr.save()

                empl = Employees(
                        user=usr,
                        name=data['firstname'],
                        lastName=data['lastname'],
                        fatherName=data['fatherName'],
                        phone=data['phone'],
                        mail=data['mail'],
                        position=data['position'],
                        status="active",
                        dateBirdth=data['dateBirdth'],
                        department=data['department']
                    )
                empl.save()

                message = f"Сотрудник {data['firstname']} {data['lastname']} создан!"

                context["message"] = message
                return render(request, "settings.html", context)

            except ValidationError as ve:
                message = f"Ошибка валидации данных: {ve}"
                context["message"] = message
                return render(request, "settings.html", context)

            except IntegrityError:
                message = "Ошибка базы данных. Возможно, пользователь или сотрудник с такими данными уже существует."
                context["message"] = message
                return render(request, "settings.html", context)


    return render(request, "settings.html", context)

@login_required
@position_required('linear')
def SettingsPageLinear(request):
    employee = request.user.employees.first()

    if employee.dateBirdth and isinstance(employee.dateBirdth, str):
        try:
            # Преобразуем строку в объект datetime, если это строка
            date_birdth_obj = datetime.strptime(employee.dateBirdth, '%Y-%m-%d')
            dateBirdth = date_birdth_obj.strftime('%Y-%m-%d')
        except ValueError:
            # Обработка ошибки, если формат даты неверен
            dateBirdth = ''
    elif employee.dateBirdth:
        # Если это уже объект даты, то просто форматируем его
        dateBirdth = employee.dateBirdth.strftime('%Y-%m-%d')

    context = {
        'name': employee.name,
        'lastName': employee.lastName,
        "fatherName": employee.fatherName,
        "phone": employee.phone,
        "email": employee.mail,
        "dateBirdth":  dateBirdth,
        "active_tab": "1"
    }

    return render(request, "settings_linear.html", context)

@login_required
def UpdateUserForm(request):
    if request.method == 'POST':
            data = request.POST
            try:
                employee = request.user.employees.first()
                if data["name"] != "" and employee.name != data["name"]:
                    employee.name = data["name"]

                if data["lastName"] != "" and employee.lastName != data["lastName"]:
                    employee.lastName = data["lastName"]

                if data["fatherName"] != "" and employee.fatherName != data["fatherName"]:
                    employee.fatherName = data["fatherName"]

                if data["phone"] != "" and employee.phone != data["phone"]:
                    employee.phone = data["phone"]

                if data["mail"] != "" and employee.mail != data["mail"]:
                    employee.mail = data["mail"]
                print(data["dateBirdth"], employee.dateBirdth)
                if data["dateBirdth"] != "" and employee.dateBirdth != data["dateBirdth"]:
                    employee.dateBirdth = data["dateBirdth"]

                employee.save()

                message = f"Данные успешо изменены!"
                dateBirdth = ''

                if employee.dateBirdth and isinstance(employee.dateBirdth, str):
                    try:
                        # Преобразуем строку в объект datetime, если это строка
                        date_birdth_obj = datetime.strptime(employee.dateBirdth, '%Y-%m-%d')
                        dateBirdth = date_birdth_obj.strftime('%Y-%m-%d')
                    except ValueError:
                        # Обработка ошибки, если формат даты неверен
                        dateBirdth = ''
                elif employee.dateBirdth:
                    # Если это уже объект даты, то просто форматируем его
                    dateBirdth = employee.dateBirdth.strftime('%Y-%m-%d')

                context = {
                    'name': employee.name,
                    'lastName': employee.lastName,
                    "fatherName": employee.fatherName,
                    "phone": employee.phone,
                    "email": employee.mail,
                    "dateBirdth": dateBirdth,
                    "edit_message": message,
                    "active_tab": "1"
                }

                if employee.position == 'top':
                    return render(request, "settings.html", context)
                elif employee.position == 'linear':
                    return render(request, "settings_linear.html", context)
            except Exception as e:
                message = f'Ошибка! Повторите позже.'

                dateBirdth = ''
                if employee.dateBirdth:
                    dateBirdth = employee.dateBirdth.strftime('%Y-%m-%d')

                context = {
                    'name': employee.name,
                    'lastName': employee.lastName,
                    "fatherName": employee.fatherName,
                    "phone": employee.phone,
                    "email": employee.mail,
                    "dateBirdth": dateBirdth,
                    "message": message,
                    "active_tab": "1"
                }
                if employee.position == 'top':
                    return render(request, "settings.html", context)
                elif employee.position == 'linear':
                    return render(request, "settings_linear.html", context)

    if employee:
        if employee.position == 'top':
            return SettingsPageTop(request)
        elif employee.position == 'linear':
            return SettingsPageLinear(request)
    return SettingsPageLinear


@login_required
def UpdatePasswordForm(request):
    employee = request.user.employees.first()
    if request.method == 'POST':
        user = request.user

        old_password = request.POST.get('lastPassword')
        new_password1 = request.POST.get('newPassword1')
        new_password2 = request.POST.get('newPassword2')

        message = ""
        if not user.check_password(old_password):
            message = 'Старый пароль неверен.'


        if new_password1 != new_password2:
            message = 'Новые пароли не совпадают.'

        if message == "":
            user.set_password(new_password1)
            user.save()

            # Обновляем сессию пользователя, чтобы не разлогинивать его
            update_session_auth_hash(request, user)
            message = 'Пароль успешно изменен.'

        context = {
            "password_message": message,
            "active_tab": "2"
        }

        if employee.position == 'top':
            return render(request, "settings.html", context)
        elif employee.position == 'linear':
            return render(request, "settings_linear.html", context)

    if employee:
        if employee.position == 'top':
            return SettingsPageTop(request)
        elif employee.position == 'linear':
            return SettingsPageLinear(request)
    return SettingsPageLinear

@login_required
def HomePageView(request):
    today = datetime.today().strftime('%d.%m.%Y')
    nextMonth = (datetime.today().replace(day=28) + timedelta(days=4)).replace(day=1)
    daysToEnd = (nextMonth - datetime.today()).days

    employee = request.user.employees.first()

    # Фильтруем виджеты по отделу и должности
    available_widgets = Widgets.objects.filter(
        departmentName=employee.department,
        positionName=employee.position
    )

    # Получаем уже выбранные виджеты
    selected_widget = EmployeeWidgets.objects.filter(employee=employee).values_list('widget', flat=True)
    selected_widgets = Widgets.objects.filter(id__in=selected_widget)
    table_data = {}
    for widget in selected_widgets:
        if widget.widgetName == "Автомобили в продаже":
            table_data[widget.id] = {
                'columns': ['Автомобиль', 'Себестоимость','Целевая цена продажи', 'Дней в продаже'],
                'data': get_cars_in_sale_widget(),
            }
        elif widget.widgetName == "Задачи":
            table_data[widget.id] = {
                'columns': ['Автомобиль', 'Задача', 'Приоритет','Дедлайн','Описание'],
                'data': get_tasks_for_employee(employee.id),
            }

    context = {'today': today,
               'daysToEnd': daysToEnd,
               'available_widgets': available_widgets,
               'selected_widget_ids': selected_widget,
               'selected_widget': selected_widgets,
               'table_data': table_data,
               }
    return render(request, "general.html", context)


def get_cars_in_sale_widget():
    cars_in_sale = Cars.objects.filter(stageId__stage='inSale')

    data = []

    for car in cars_in_sale:
        cost_price = DDS.objects.filter(carId=car, isProfit=False).aggregate(total_cost=Sum('amount'))[
                         'total_cost'] or 0

        prebuy_data = PrebuyCars.objects.filter(carId=car).first()
        if prebuy_data:
            target_price = prebuy_data.predictCost
        else:
            target_price = None

        # Формируем данные для виджета
        data.append({
            'Автомобиль': car.name,
            'Себестоимость': cost_price,
            'Целевая цена продажи': target_price
        })

    return data

def get_tasks_for_employee(employee_id):
    tasks = Tasks.objects.filter(employeeId=employee_id).select_related('carId')

    task_data = []

    for task in tasks:
        car_name = task.carId.name if task.carId else "Не указано"

        task_data.append({
            'Автомобиль': car_name,
            'Задача': task.name,
            'Приоритет': task.priority,
            'Дедлайн': task.deadline,
            'Описание': task.description
        })

    return task_data


def save_widgets_view(request):
    if request.method == 'POST':
        employee = request.user.employees.first()

        selected_widget_ids = request.POST.getlist('widgets')

        employee_widgets = EmployeeWidgets.objects.filter(employee=employee)
        if employee_widgets.exists():
            employee_widgets.delete()

        empWid = EmployeeWidgets(employee=employee)
        empWid.save()

        if selected_widget_ids:
            widgets = Widgets.objects.filter(id__in=selected_widget_ids)
            if widgets.exists():
                empWid.widget.set(widgets)

        return HomePageView(request)


def LogoutView(request):
    logout(request)
    return redirect("login_page")

@login_required
def SettingsPageView(request):
    employee = request.user.employees.first()  # Получаем первого сотрудника

    if employee:  # Проверяем, существует ли сотрудник
        if employee.position == 'top':
            return SettingsPageTop(request)
        elif employee.position == 'linear':
            return SettingsPageLinear(request)


def get_models(request, brand_name):
    brand = get_object_or_404(Brand, name=brand_name)

    brand_models = BrandModel.objects.filter(brand_id=brand.id).select_related('model')

    # Извлекаем необходимые данные
    data = [{'id': brand_model.model.id, 'name': brand_model.model.name} for brand_model in brand_models]

    return JsonResponse(data, safe=False)

def CarCardView(request, car_id):
    car = get_object_or_404(Cars, id=car_id)
    buyInfo = BuyCars.objects.filter(carId=car_id)
    prebuyInfo = PrebuyCars.objects.filter(carId=car_id)
    context = {
        'car': car,
        'buyCar': buyInfo,
        'preBuyCar': prebuyInfo,
    }
    return render(request, 'car_card.html', context)

@login_required
def TradehubFormView(request):
    brebuyCars = Cars.objects.filter(stageId=5)
    saleCars = Cars.objects.exclude(stageId__in=[2, 3, 5])
    brands = Brand.objects.all()
    models = Model.objects.all()
    ddsAccounts = DDSAccounts.objects.all()
    clientSources = ClientSources.objects.all()
    moneyArcticles = MoneyArticles.objects.all()
    entities = Entities.objects.all()
    employee = Employees.objects.all()
    stage = KanbanCols.objects.exclude(id__in=[2, 3, 5])

    context = {
        'brands': brands,
        'models': models,
        "ddsAccounts": ddsAccounts,
        "moneyArticles": moneyArcticles,
        "clientSources": clientSources,
        "entities": entities,
        "cars": brebuyCars,
        "sale_cars": saleCars,
        'task_employee': employee,
        'task_stage': stage,
        "active_tab": "1"
    }

    return render(request, 'form.html', context)


def TradehubFormSecondView(request, message, activeTab, paramName):
    brebuyCars = Cars.objects.filter(stageId=5)
    saleCars = Cars.objects.exclude(stageId__in=[2, 3, 5])
    brands = Brand.objects.all()
    models = Model.objects.all()
    ddsAccounts = DDSAccounts.objects.all()
    clientSources = ClientSources.objects.all()
    moneyArcticles = MoneyArticles.objects.all()
    entities = Entities.objects.all()
    employee = Employees.objects.all()
    stage = KanbanCols.objects.exclude(id__in=[2, 3, 5])

    context = {
        'brands': brands,
        'models': models,
        "ddsAccounts": ddsAccounts,
        "moneyArticles": moneyArcticles,
        "clientSources": clientSources,
        "entities": entities,
        "cars": brebuyCars,
        "sale_cars":saleCars,
        'task_employee': employee,
        'task_stage': stage,
        "active_tab":activeTab,
        f"{paramName}": message
    }


    return render(request, 'form.html', context)


def PreBuyCarForm(request):
    if request.method == 'POST':
            data = request.POST
            try:
                car = Cars(
                    stageId = KanbanCols.objects.get(id=5),
                    brand = data['mark'],
                    model = data['model'],
                    VIN = data['vin'],
                    year = int(data['year']),
                    odometer = int(data['mileage']),
                    engine = data['engine'],
                    transmission = data['transmission'],
                    name = data['mark'] + " " + data['model'] + " " + data['year'] + data['vin'][-4:]
                )
                car.save()

                current_user = request.user
                employee = get_object_or_404(Employees, user=current_user)

                preBuyCar = PrebuyCars(
                    carId =  car,
                    employeeId = employee,
                    prebuyDate = date.today(),
                    rank = int(data['haraba']),
                    carSourse = data['source'],
                    description = data['description'],
                    carCost = int(data['cost']),
                    marginality = (data['margin']),
                    predictCost = (data['sale_forecast']),
                    liquidRatio = int(data['current_listings'])/int(data['sold_last_3_months']),
                )

                preBuyCar.save()

                message = f"Автомобиль {data['mark']} {data['model']} {data['year']} {data['vin'][-4:]} создан!"
                return TradehubFormSecondView(request, message,"1","message")
            except Exception as e:
                message = f'Ошибка при создании предпокупки: {str(e)}'
                return TradehubFormSecondView(request, message, "1", "message")

    message = f"Ошибка если не POST!"
    return TradehubFormSecondView(request, message,"1","message")

def BuyCarForm(request):
    if request.method == 'POST':
        data = request.POST

        current_user = request.user
        employee = get_object_or_404(Employees, user=current_user)

        if data['action'] == 'waiting':
            try:
                car = Cars.objects.get(id=int(data['buy_car_id']))

                dds = DDS(
                    carId=car,
                    employeeId = employee,
                    article = "buycar",
                    operationDate = date.today(),
                    amount = int(data['buy_car_amount']),
                    paymentAccount = data['buy_car_account_name'],
                    isProfit = False
                )
                dds.save()

                buyCar = BuyCars(
                    carId=car,
                    entityId = Entities.objects.get(id=int(data['buy_car_entitie'])),
                    ddsId = dds,
                    owners = int(data['buy_car_owners']),
                    typePTS = data['buy_car_pts'],
                    cntKeys = int(data['buy_car_keys'])
                )
                buyCar.save()

                message = f"Автомобиль {car.name} куплен!"
                return TradehubFormSecondView(request, message,"2","buy_message")
            except Exception as e:
                message = f'Ошибка при создании предпокупки: {str(e)}'
                return TradehubFormSecondView(request, message,"2","buy_message")

        elif data['action'] == 'prebuy':
            try:
                car = Cars(
                    stageId = KanbanCols.objects.get(id=6),
                    brand = data['buy_car_mark'],
                    model = data['buy_car_model'],
                    VIN = data['buy_car_vin'],
                    year = int(data['buy_car_year']),
                    odometer = int(data['buy_car_mileage']),
                    engine = data['buy_car_engine'],
                    transmission = data['buy_car_transmission'],
                    name = data['buy_car_mark'] + " " + data['buy_car_model'] + " " + data['buy_car_year'] + data['buy_car_vin'][-4:]
                )
                car.save()

                preBuyCar = PrebuyCars(
                    carId =  car,
                    employeeId = employee,
                    prebuyDate = date.today(),
                    rank = int(data['buy_car_haraba']),
                    carSourse = data['buy_car_source'],
                    description = data['buy_car_description'],
                    carCost = int(data['buy_car_prebuy_amount']),
                    marginality = (data['buy_car_margin']),
                    predictCost = (data['buy_car_sale_forecast']),
                    liquidRatio = int(data['buy_car_current_listings'])/int(data['buy_car_sold_last_3_months']),
                )
                preBuyCar.save()

                dds = DDS(
                    carId=car,
                    employeeId=employee,
                    article="buycar",
                    operationDate=date.today(),
                    amount=int(data['buy_car_prebuy_amount']),
                    paymentAccount=data['buy_car_prebuy_account_name'],
                    isProfit=False
                )
                dds.save()

                buyCar = BuyCars(
                    carId=car,
                    entityId=Entities.objects.get(id=int(data['buy_car_entitie'])),
                    ddsId=dds,
                    owners=int(data['buy_car_prebuy_owners']),
                    typePTS=data['buy_car_prebuy_pts'],
                    cntKeys=int(data['buy_car_prebuy_keys'])
                )
                buyCar.save()
                message = f"Автомобиль {data['buy_car_mark']} {data['buy_car_model']} {data['buy_car_year']} {data['buy_car_vin'][-4:]} создан!"
                return TradehubFormSecondView(request, message,"2","buy_message")
            except Exception as e:
                message = f'Ошибка при создании покупки: {str(e)}'
                return TradehubFormSecondView(request, message,"2","buy_message")

    message = f"Ошибка если не POST!"
    return TradehubFormSecondView(request, message,"2","buy_message")


def SaleCarForm(request):
    if request.method == 'POST':
        data = request.POST
        current_user = request.user
        employee = get_object_or_404(Employees, user=current_user)

        try:
            car = get_object_or_404(Cars, id=int(data['sale_car_id']))
            kanban_stage = get_object_or_404(KanbanCols, id=2)
            car.stageId = kanban_stage
            car.save()

            dds = DDS(
                carId=car,
                employeeId=employee,
                article="salecar",
                operationDate=date.today(),
                amount=int(data['sale_cost']),
                paymentAccount=data['sale_account_name'],
                isProfit=True
            )
            dds.save()

            sale_message = f"Автомобиль {car.name} продан!"
            return TradehubFormSecondView(request, sale_message,"3","sale_message")
        except Exception as e:
            sale_message = f'Ошибка при продаже: {str(e)}'
            return TradehubFormSecondView(request, sale_message,"3","sale_message")

    sale_message = f'Не POST запрос'
    return TradehubFormSecondView(request, sale_message,"3","sale_message")

def TaskForm(request):
    if request.method == 'POST':
        data = request.POST

        try:
            task_car_id = data['task_car_id']
            task_employee_id = data['task_employee_id']
            task_stage_id = data['task_stage_id']
            task_name = data['task_name']
            task_priority = data['task_priority']
            task_description = data['task_description']
            task_deadline = data['task_deadline']

            # Создаем новую задачу
            task = Tasks(
                carId=Cars.objects.get(id=task_car_id),
                employeeId=Employees.objects.get(id=task_employee_id),
                stageId=KanbanCols.objects.get(id=task_stage_id),
                name=task_name,
                priority=task_priority,
                description=task_description,
                deadline=task_deadline,
                status="active",
                taskDate= date.today(),
            )
            task.save()

            task_message = f"Задача создана!"
            return TradehubFormSecondView(request, task_message,"7","task_message")
        except Exception as e:
            task_message = f'Ошибка: {str(e)}'
            return TradehubFormSecondView(request, task_message,"7","task_message")

    task_message = f'Не POST запрос'
    return TradehubFormSecondView(request, task_message,"7","task_message")

@login_required
def StockPageView(request):
    cars = Cars.objects.select_related('stageId',).exclude(
        stageId__name__in=['sale', 'trash', 'buywait']
    )

    # Собираем информацию для каждой машины
    car_data = []
    for car in cars:
        # Получаем цену закупа из PrebuyCars
        prebuy = PrebuyCars.objects.filter(carId=car).first()

        # Подсчет затрат из DDS (сумма всех, где isProfit = False)
        expenses = DDS.objects.filter(carId=car, isProfit=False).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

        # Себестоимость = цена закупа + затраты
        cost_price = prebuy.carCost + expenses if prebuy else 0

        car_data.append({
            'car': car,
            'prebuy': prebuy,
            'expenses': expenses,
            'cost_price': cost_price,
        })

    return render(request, 'sclad.html', {'car_data': car_data})

@login_required
@position_required('top')
def AnalitycPageView(request):
    return render(request, 'analytics.html')

@login_required
@position_required('top')
def generate_analytics_view(request):
    if request.method == 'POST':
        # Извлекаем диапазон дат из формы
        date_range = request.POST.get('date-range', '')
        print(date_range)
        start_date, end_date = date_range.split(' to ')

        # Преобразуем строки в даты
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Получаем финансовые показатели по месяцам
        monthly_metrics = calculate_monthly_financial_metrics(start_date, end_date)
        print(monthly_metrics)
        context = {
            'monthly_metrics': monthly_metrics
        }

        return render(request, 'analytics.html', context)


def month_range(start_date, end_date):
    """Генерация всех месяцев между двумя датами."""
    current_date = start_date.replace(day=1)
    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        last_day = calendar.monthrange(year, month)[1]  # Последний день текущего месяца
        yield current_date, current_date.replace(day=last_day)
        next_month = current_date.month % 12 + 1
        next_year = current_date.year + (current_date.month // 12)
        current_date = current_date.replace(year=next_year, month=next_month, day=1)

def calculate_monthly_financial_metrics(start_date, end_date):
    # Словарь для хранения данных по месяцам
    monthly_data = []

    # Перебираем каждый месяц в диапазоне
    for month_start, month_end in month_range(start_date, end_date):
        print(month_start, month_end)
        # Выручка = сумма всех доходных операций (isProfit=True) за месяц
        revenue = DDS.objects.filter(
            operationDate__range=[month_start, month_end],
            isProfit=True
        ).aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0

        # Расходные операции = сумма всех расходных операций (isProfit=False) за месяц
        expenses = DDS.objects.filter(
            operationDate__range=[month_start, month_end],
            isProfit=False
        ).aggregate(total_expenses=Sum('amount'))['total_expenses'] or 0

        # Дополнительные расходы (carId пустой) за месяц
        additional_expenses = DDS.objects.filter(
            operationDate__range=[month_start, month_end],
            carId__isnull=True
        ).aggregate(total_additional_expenses=Sum('amount'))['total_additional_expenses'] or 0

        # Валовая прибыль = выручка - расходные операции
        gross_profit = revenue - expenses

        # Операционная прибыль = валовая прибыль - расходы (carId пустой)
        operating_profit = gross_profit - additional_expenses

        # Операционная рентабельность = операционная прибыль / выручку * 100%
        operating_margin = (operating_profit / revenue * 100) if revenue > 0 else 0

        # Рентабельность товара
        product_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
        print(revenue)
        # Добавляем данные за текущий месяц
        monthly_data.append({
            'month': month_start.strftime('%B %Y'),  # Название месяца и год
            'revenue': revenue,
            'gross_profit': gross_profit,
            'expenses': expenses,
            'operating_profit': operating_profit,
            'operating_margin': operating_margin,
            'product_margin': product_margin
        })

    # Рассчитываем сальдо (итоговые данные за весь период)
    total_revenue = sum([month['revenue'] for month in monthly_data])
    total_gross_profit = sum([month['gross_profit'] for month in monthly_data])
    total_expenses = sum([month['expenses'] for month in monthly_data])
    total_operating_profit = sum([month['operating_profit'] for month in monthly_data])

    # Добавляем итоговую строку (сальдо)
    monthly_data.append({
        'month': 'Сальдо',
        'revenue': total_revenue,
        'gross_profit': total_gross_profit,
        'expenses': total_expenses,
        'operating_profit': total_operating_profit,
        'operating_margin': (total_operating_profit / total_revenue * 100) if total_revenue > 0 else 0,
        'product_margin': (total_gross_profit / total_revenue * 100) if total_revenue > 0 else 0
    })

    return monthly_data