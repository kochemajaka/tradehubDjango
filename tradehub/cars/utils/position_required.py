from .imports import *
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