from django import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
import barkeeper.views as views 

urlpatterns = [
    path('', views.index, name='home'),
    path('camera/', views.camera_start, name='camera_start'),
    path('loadcell/', views.loadcell_start, name='loadcell_start'),
    path('robot/', views.robot_homing, name='robot_homing'),
    path('robot/grab', views.robot_homing, name='robot_grab'),
    path('robot/pour', views.robot_homing, name='robot_pour'),
    path('event/create', views.event_create, name='event_create'),
    path('api/event/', views.BarkeepingHistory.as_view(), name='api_event_history'),
    path('api/event/<int:pk>/', views.BarkeepingDetail.as_view(), name='api_event_detail'),
    path('api/users/', views.UserList.as_view(), name='api_users'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='api_user_detail'),
    path('__debug__/', include('debug_toolbar.urls'))
]
urlpatterns = format_suffix_patterns(urlpatterns)