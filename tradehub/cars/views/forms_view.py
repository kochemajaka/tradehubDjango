from ..utils.position_required import position_required
from ..utils.imports import *

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

def get_models(request, brand_name):
    brand = get_object_or_404(Brand, name=brand_name)

    brand_models = BrandModel.objects.filter(brand_id=brand.id).select_related('model')

    # Извлекаем необходимые данные
    data = [{'id': brand_model.model.id, 'name': brand_model.model.name} for brand_model in brand_models]

    return JsonResponse(data, safe=False)