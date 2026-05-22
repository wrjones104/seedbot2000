from django.urls import path
from . import views
from . import api_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('tune-up/', views.tune_up_view, name='tune-up'),
    path('presets/', views.preset_list_view, name='preset-list'),    
    path('profile/', views.my_profile_view, name='my-profile'),
    path('create/', views.preset_create_view, name='preset-create'),
    path('quick-roll/', views.quick_roll_view, name='quick-roll'),
    path('tune-up/', views.tune_up_view, name='tune-up'),
    path('tune-up/api/', views.tune_up_api_view, name='tune-up-api'), 
    path('tune-up/status/<str:task_id>/', views.tune_up_status_view, name='tune-up-status'),
    path('api/update_sotw_preset/', views.update_sotw_preset_view, name='api-update-sotw'),
    path('api/v1/seed/generate', api_views.SeedGenerateAPIView.as_view(), name='api-seed-generate'),
    path('api/v1/seed/status/<str:task_id>/', api_views.SeedStatusAPIView.as_view(), name='api-seed-status'),
    path('api/v1/seed/<str:task_id>/download', api_views.SeedDownloadAPIView.as_view(), name='api-seed-download'),
    path('api-key/create/', views.create_api_key_view, name='api-key-create'),
    path('api-key/delete/<int:key_id>/', views.delete_api_key_view, name='api-key-delete'),
    path('roll-status/<str:task_id>/', views.get_local_seed_roll_status_view, name='get-local-seed-roll-status'),
    path('<path:pk>/update/', views.preset_update_view, name='preset-update'),
    path('<path:pk>/delete/', views.preset_delete_view, name='preset-delete'),
    path('<path:pk>/toggle-feature/', views.toggle_feature_view, name='toggle-feature'),
    path('<path:pk>/toggle-favorite/', views.toggle_favorite_view, name='toggle-favorite'),
    path('<path:pk>/roll/', views.roll_seed_dispatcher_view, name='roll-seed'),
    path('<path:pk>/make-yaml/', views.make_yaml_view, name='make-yaml'),
    path('<path:pk>/', views.preset_detail_view, name='preset-detail'),
    path('preset-status/<path:pk>/', views.preset_status_view, name='preset-status'),
]