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
from cars import views

urlpatterns = [
    path('admin/', admin.site.urls, name="admin_page"),
    path('login', views.TradehubLoginView.as_view(), name="login_page"),
    path('logout/', views.LogoutView, name="logout"),
    path('home', views.HomePageView, name="home"),
    path('settings', views.SettingsPageView, name="settings"),
    path('form', views.TradehubFormView, name="form_page"),
    path('stock', views.StockPageView, name="sclad_page"),
    path('car_card/<int:car_id>/', views.CarCardView, name='car_card'),
    path('get_models/<brand_name>/', views.get_models, name='get_models'),
    path('prebuy_form', views.PreBuyCarForm, name='prebuy_form'),
    path('buy_form', views.BuyCarForm, name='buy_form'),
    path('sale_form', views.SaleCarForm, name='sale_form'),
    path('task_form', views.TaskForm, name='task_form'),
    path('save_widgets/', views.save_widgets_view, name='save_widgets'),
    path('analytics', views.AnalitycPageView, name='analytics'),
    path('analytics/pnl', views.generate_analytics_view, name='generate_pnl'),
    path('settings/update/password', views.UpdateUserForm, name='update_user_info'),
    path('settings/update/userinfo', views.UpdatePasswordForm, name='update_password'),
    path('settings/update/adduser', views.AddUserForm, name='add_user'),
    path('kanban', views.KanbanPageView, name='kanban'),
    path('update-stage/', views.UpdateStage, name='update_stage'),
    path('kanban/tasks/<int:car_id>/', views.GetTasks, name='get_tasks_by_car'),
    path('kanban/tasks/complete/', views.CompleteTasks, name='complete_tasks'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
