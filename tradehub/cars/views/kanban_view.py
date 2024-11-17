from ..utils.position_required import position_required
from ..utils.imports import *
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