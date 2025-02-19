from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('certificateadm/', certificate_adm, name='certificateadm'),
    path('loginadm/', login_adm, name='loginadm'),
    path('logoutadm/', logout_viewadm, name='logoutadm'),
    path('regadm/', reg_adm, name='regadm'),
    path('dashboardadm/', dashboard_adm, name='dashboardadm'),
    path('', dashboard_adm, name='dashboardadm'),
    path('approvecertificate/', approve_certificate, name='approvecertificate'),
    path('deletecertificate/', delete_certificate, name='deletecertificate'),


    path('plantationdatapvtadm/', plantationdata_pvt_adm, name='plantationdatapvtadm'),
    path('plantationdatangoadm/', plantationdata_ngo_adm, name='plantationdatangoadm'),
    path('plantationdatagovadm/', plantationdata_gov_adm, name='plantationdatagovadm'),


    path('download-plantation/', views.download_plantation_csv, name='download_plantation_csv'),
    path('refresh-data/', views.execute_sql, name='refresh_data'),  # New URL for refreshing
    path('download_kmz/', views.download_kmz, name='download_kmz'),

    


]