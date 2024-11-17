from .home_view import HomePageView, get_tasks_for_employee, get_cars_in_sale_widget, save_widgets_view
from .analytics_view import AnalitycPageView, generate_analytics_view
from .auth_view import TradehubLoginView, LogoutView
from .forms_view import TradehubFormView, TradehubFormSecondView, TaskForm, SaleCarForm, BuyCarForm, PreBuyCarForm, get_models
from .kanban_view import KanbanPageView, UpdateStage, CompleteTasks, GetTasks
from .settings_view import SettingsPageView, SettingsPageLinear, SettingsPageTop, AddUserForm, UpdateUserForm, UpdatePasswordForm
from .storage_view import StockPageView, CarCardView

__all__ = [
    'TradehubLoginView',
    'LogoutView',
    'HomePageView',
    'get_tasks_for_employee',
    'get_cars_in_sale_widget',
    'save_widgets_view',
    'AnalitycPageView',
    'generate_analytics_view',
    'TradehubFormView',
    'TradehubFormSecondView',
    'TaskForm',
    'SaleCarForm',
    'BuyCarForm',
    'PreBuyCarForm',
    'get_models',
    'KanbanPageView',
    'UpdateStage',
    'CompleteTasks',
    'GetTasks',
    'SettingsPageView',
    'SettingsPageLinear',
    'SettingsPageTop',
    'AddUserForm',
    'UpdateUserForm',
    'UpdatePasswordForm',
    'StockPageView',
    'CarCardView'
]