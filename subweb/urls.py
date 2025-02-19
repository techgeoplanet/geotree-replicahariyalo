from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('accounts/login/', tempuser_login, name='tempuser_login'),
    path('customuser-login/', customuser_login, name='customuser_login'),
    path('customuser-register/', customuser_register, name='customuser_register'),
    path('add-tempdata/', add_tempdata, name='add_tempdata'),


    path('logout/', logout_view, name='logout_view'),


    path('', views.hi_home_page, name='hi-home'),
    path('home/', views.home_page, name='home'),
    path('hi/home/', views.hi_home_page, name='hi-home'),
    path('addplant/', views.addplant_normaluser_page, name='addplant'),
    path('hi/addplant/', views.hi_addplant_normaluser_page, name='hi-addplant'),
    path('rewards/', views.rewards_viewset, name='rewards'),
    path('hi/rewards/', views.hi_rewards_viewset, name='hi-rewards'),
    path('plantationtips/', views.tips_viewset, name='plantationtips'),
    path('hi/plantationtips/', views.hi_tips_viewset, name='hi-plantationtips'),


    # path('checkcam/', views.checkcam, name='checkcam'),
    # path('certificate-generator/', views.certificate_generator, name='certificate_generator'),
    path('get_certificate_template/', views.get_certificate_template, name='get_certificate_template'),

    path('plantation_bypvt/', views.CreatePlantationPvtView.as_view(), name='plantation_bypvt'),
    path('plantation_bygov/', views.CreatePlantationGovView.as_view(), name='plantation_bygov'),
    path('plantation_byngo/', views.CreatePlantationNgoView.as_view(), name='plantation_byngo'),


    path('my_pvt_history/', views.my_pvt_history_viewset, name='my_pvt_history'),
    path('my_gov_history/', views.my_gov_history_viewset, name='my_gov_history'),
    path('my_ngo_history/', views.my_ngo_history_viewset, name='my_ngo_history'),

    path('hi/my_pvt_history/', views.hi_my_pvt_history_viewset, name='hi-my_pvt_history'),
    path('hi/my_gov_history/', views.hi_my_gov_history_viewset, name='hi-my_gov_history'),
    path('hi/my_ngo_history/', views.hi_my_ngo_history_viewset, name='hi-my_ngo_history'),

    path('postCerti/', views.CreateTempStorageCertificateInfoView.as_view(), name='postCerti'),

    path('moreinformation/', views.moreinformation_viewset, name='moreinformation'),
    path('hi/moreinformation/', views.hi_moreinformation_viewset, name='hi-moreinformation'),

    path('save_certificate_info/', views.save_certificate_info, name='save_certificate_info'),
    path('certificate/', views.certificate_view, name='certificate'),
    path('hi/certificate/', views.hi_certificate_view, name='hi-certificate'),

]
