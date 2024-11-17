from ..utils.position_required import position_required
from ..utils.imports import *
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
