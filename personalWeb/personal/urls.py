from django.urls import path
from . import views


urlpatterns = [
    path('', views.Default.home, name='index'),
    path('generic/', views.generic, name='generic'),
    path('elements/', views.elements, name='elements'),
    # User verification paths
    path('login/', views.UserInformation.login_user, name='login'),
    path('registration/', views.UserInformation.register, name='registration'),
    path('profile/', views.UserInformation.profile, name='profile'),
    path('logout/', views.UserInformation.user_logout, name='logout'),
    # Finance paths
    path('finances/', views.Finance.finances, name='finances'),
    path('transact/', views.deposit_withdrawal, name='depo'),
    path('bank registration/', views.Finance.bank_registration, name='bank_reg'),
    path('history/', views.Finance.history, name='history'), 
]
