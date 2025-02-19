from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Geotree Dashboard"
admin.site.site_title = "Geotree Dashboard"
admin.site.site_url= "Geotree"
admin.site.index_title = "Dashboard"

urlpatterns = [
    path('admin-django/', admin.site.urls),
    path('api/user/', include('account.urls')),
    path('api/', include('api.urls')),
    path('api-nursery/', include('api_nursery.urls')),
    path('',include('subweb.urls')),
    path('admin/', include('admindashboard.urls')),
    path('portaldash/', include('portaldash.urls')),
    path('map/', include('map.urls')),
    path('update-phase/', include('update_app.urls')),
    path('scan/',include('publicqrcode.urls')),
]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_URL)

else :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
