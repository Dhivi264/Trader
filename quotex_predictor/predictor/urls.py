from django.urls import path
from . import views

urlpatterns = [
    # Main chart upload interface
    path('', views.index, name='index'),
    
    # Chart Analysis Endpoints
    path('api/upload-chart-analysis/', views.upload_chart_analysis, name='upload_chart_analysis'),
    path('api/chart-analyses/', views.get_chart_analyses, name='chart_analyses'),
    path('api/chart-analysis-detail/<int:chart_id>/', views.get_chart_analysis_detail, name='chart_analysis_detail'),
    path('api/delete-chart-analysis/<int:chart_id>/', views.delete_chart_analysis, name='delete_chart_analysis'),
]