from django import views
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
import barkeeper.views as views 

urlpatterns = [
    path('', views.index, name='home'),
    path('camera/', views.camera_start, name='camera_start'),
    path('camera/ocr', views.camera_ocr, name='camera_ocr'),
    path('loadcell/', views.loadcell_start, name='loadcell_start'),
    path('robot/', views.robot_homing, name='robot_homing'),
    path('robot/homing', views.robot_homing, name='robot_homing'),
    path('robot/grab', views.robot_grab, name='robot_grab'),
    path('robot/pour', views.robot_pour, name='robot_pour'),
    path('robot/kinematics/forward', views.robot_kinematics_forward, name='robot_kinematics_forward'),
    path('robot/kinematics/forward/result', views.robot_kinematics_forward_result, name='robot_kinematics_forward_result'),
    path('robot/kinematics/inverse', views.robot_kinematics_inverse, name='robot_kinematics_inverse'),
    path('robot/kinematics/inverse/result', views.robot_kinematics_inverse_result, name='robot_kinematics_inverse_result'),
    path('event/create', views.event_create, name='event_create'),
    path('event/<int:pk>', views.event_read, name='event_read'),
    path('event/<int:pk>/update', views.event_update, name='event_update'),
    path('event/<int:pk>/delete', views.event_delete, name='event_delete'),
    path('event/history', views.event_history, name='event_history'),
    path('api/event/', views.BarkeepingHistory.as_view(), name='api_event_history'),
    path('api/event/<int:pk>/', views.BarkeepingDetail.as_view(), name='api_event_detail'),
    path('api/users/', views.UserList.as_view(), name='api_users'),
    path('api/users/<int:pk>/', views.UserDetail.as_view(), name='api_user_detail'),
    path('__debug__/', include('debug_toolbar.urls'))
    ]

urlpatterns = format_suffix_patterns(urlpatterns)