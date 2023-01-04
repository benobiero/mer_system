
from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt
from .views import DashbordCharts

urlpatterns = [
    path('', views.home,name='home'),
    path('project-dashboard', views.project_dashboard,name='project-dashboard'),
    path('add-project', views.add_project,name='add-project'),
    path('search-grants', csrf_exempt(views.search_grant),
         name="serach-grants"),
    path('test', csrf_exempt(views.test),
         name="test"),
    path('reporting-tools', views.reporting_tools,name='reporting-tools'),
    path('monthly-tool', views.monthly_tool,name='monthly-tool'),
    path('preview-monthly', views.preview_monthly,name='preview-monthly'),
    path('dashboard', csrf_exempt(views.dashboard),name='dashboard'),
    path('dashboard-charts', DashbordCharts.as_view(),name='dashboard-charts'),
    path('unaccomplished', views.unaccomplished,name='unaccomplished'),
    path('under-review', views.monthly_report,name='under-review'),
    path('month-report-detail/<int:pk>', views.month_report_detail,name='month-report-detail'),
    path('data-entry', views.data_entry,name='data-entry')
    
 

]




    
