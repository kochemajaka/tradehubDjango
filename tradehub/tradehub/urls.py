"""
URL configuration for tradehub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
import django.contrib.auth.views as authView
from django.conf import settings
from django.conf.urls.static import static
from cars.views import *

urlpatterns = [
    path('admin/', admin.site.urls, name="admin_page"),
    path('login', TradehubLoginView.as_view(), name="login_page"),
    path('logout/', LogoutView, name="logout"),
    path('home', HomePageView, name="home"),
    path('settings', SettingsPageView, name="settings"),
    path('form', TradehubFormView, name="form_page"),
    path('stock', StockPageView, name="sclad_page"),
    path('car_card/<int:car_id>/', CarCardView, name='car_card'),
    path('get_models/<brand_name>/', get_models, name='get_models'),
    path('prebuy_form', PreBuyCarForm, name='prebuy_form'),
    path('buy_form', BuyCarForm, name='buy_form'),
    path('sale_form', SaleCarForm, name='sale_form'),
    path('task_form', TaskForm, name='task_form'),
    path('save_widgets/', save_widgets_view, name='save_widgets'),
    path('analytics', AnalitycPageView, name='analytics'),
    path('analytics/pnl', generate_analytics_view, name='generate_pnl'),
    path('settings/update/password', UpdateUserForm, name='update_user_info'),
    path('settings/update/userinfo', UpdatePasswordForm, name='update_password'),
    path('settings/update/adduser', AddUserForm, name='add_user'),
    path('kanban', KanbanPageView, name='kanban'),
    path('update-stage/', UpdateStage, name='update_stage'),
    path('kanban/tasks/<int:car_id>/', GetTasks, name='get_tasks_by_car'),
    path('kanban/tasks/complete/', CompleteTasks, name='complete_tasks'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
