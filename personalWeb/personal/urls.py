from django.urls import path
from . import views


urlpatterns = [
    path('', views.Default.home, name='index'),
    path('generic/', views.generic, name='generic'),
    path('elements/', views.elements, name='elements'),
    # User verification paths
    path('login', views.UserInformation.login_user, name='login'),
    path('registration/', views.UserInformation.register, name='registration'),
    path('profile/', views.UserInformation.profile, name='profile'),
    path('logout/', views.UserInformation.user_logout, name='logout'),
    # Finance paths
    path('finances/', views.Finance.finances, name='finances'),
    path('transact/', views.deposit_withdrawal, name='depo'),
    path('bank registration/', views.Finance.bank_registration, name='bank_reg'),
    path('history/', views.Finance.history, name='history'),
    path('Buy/', views.Commerce.default, name='commerce'),
    # chess paths
    path('Chess/', views.Default.lichess, name='chess'),
    # betting paths
    path('Gambling/', views.Gambling.as_view(), name='bet'),
    path('Slips/', views.Gambling.as_view(), name='slips'),
    path('lichess/', views.Default.lichess, name='chess'),
]
