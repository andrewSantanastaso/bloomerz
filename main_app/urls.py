from django.urls import path
from . import views
# from main_app.views import 

urlpatterns = [
    path('', views.home, name='home'),
    path('gardens/', views.garden_index, name='garden-index'),
    path('gardens/<int:pk>/', views.garden_detail.as_view(), name='garden-detail'),
    path('gardens/create/', views.GardenCreate.as_view(), name='garden-create'),
    path('gardens/<int:pk>/update/', views.GardenUpdate.as_view(), name='garden-update'),
    path('gardens/<int:pk>/delete/', views.GardenDelete.as_view(), name='garden-delete'),
    path('plots/', views.plot_index, name='plot-index'),
    path('gardens/<int:garden_id>/plots/create', views.CreatePlot.as_view(), name='plot-create'),
    path('plots/<int:plot_id>', views.plot_detail, name='plot-detail'),
    path('plots/<int:pk>/update', views.UpdatePlot.as_view(), name='plot-update'),
    path('plots/<int:plot_id>/water', views.water_plot, name='plot-water'),
    path('plots/<int:plot_id>/delete', views.plot_delete, name='plot-delete'),
    path('plants/', views.plant_index, name='plant-index'),
    path('gardens/<int:garden_id>/plots/<int:plot_id>/plants/create', views.CreatePlant.as_view(), name='plant-create'),
    path('gardens/<int:garden_id>/plots/<int:plot_id>/plants/<int:plant_id>', views.PlantDetail.as_view(), name='plant-detail'),
    path('gardens/<int:garden_id>/plots/<int:plot_id>/plants/<int:pk>/update', views.UpdatePlant.as_view(), name='plant-update'),
    path('gardens/<int:garden_id>/plots/<int:plot_id>/plants/<int:pk>/delete', views.DeletePlant.as_view(), name='plant-delete'),
    path('signup/', views.signup, name='signup'),
    
    
]