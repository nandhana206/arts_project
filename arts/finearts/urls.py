from django.urls import path
from finearts import views

urlpatterns = [
    path('', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('user_profile/', views.user_profile_view, name='user_profile'),
    path('logout/',views.logout_view,name='logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]       