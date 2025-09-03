from django.urls import path
from . import views

urlpatterns = [
    path('', views.preset_list_view, name='webapp-list'),
    path('profile/', views.my_profile_view, name='my-profile'),
    path('create/', views.preset_create_view, name='preset-create'),
    path('roll-status/<str:task_id>/', views.get_local_seed_roll_status_view, name='get-local-seed-roll-status'),
    path('<path:pk>/update/', views.preset_update_view, name='preset-update'),
    path('<path:pk>/delete/', views.preset_delete_view, name='preset-delete'),
    path('<path:pk>/toggle-feature/', views.toggle_feature_view, name='toggle-feature'),
    path('<path:pk>/toggle-favorite/', views.toggle_favorite_view, name='toggle-favorite'),
    path('<path:pk>/roll/', views.roll_seed_dispatcher_view, name='roll-seed'),
    path('<path:pk>/', views.preset_detail_view, name='preset-detail'),
]