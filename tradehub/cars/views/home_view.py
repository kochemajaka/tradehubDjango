from ..utils.position_required import position_required
from ..utils.imports import *
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
