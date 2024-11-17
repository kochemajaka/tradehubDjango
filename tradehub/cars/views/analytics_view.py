from ..utils.position_required import position_required
from ..utils.imports import *

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