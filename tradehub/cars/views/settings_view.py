from ..utils.position_required import position_required
from ..utils.imports import *

@login_required
def SettingsPageView(request):
    employee = request.user.employees.first()  # Получаем первого сотрудника

    if employee:  # Проверяем, существует ли сотрудник
        if employee.position == 'top':
            return SettingsPageTop(request)
        elif employee.position == 'linear':
            return SettingsPageLinear(request)

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
