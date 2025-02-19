from django.contrib import admin
from .models import QrcodeVisiter
from rangefilter.filters import DateRangeFilter

@admin.register(QrcodeVisiter)
class QrcodeVisiterAdmin(admin.ModelAdmin):
    list_display = ('id', 'qrcode', 'timestamp')  # Columns in admin panel
    list_per_page = 20  # Paginate records in admin panel
    search_fields = ('qrcode',)  # Enable search by qrcode
    list_filter = (
        ('timestamp', DateRangeFilter),  # Filter for date range
    )

    def total_visitors(self, request):
        count = QrcodeVisiter.objects.count()
        return f"Total Visitors: {count}"

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['total_visitors'] = QrcodeVisiter.objects.count()
        return super().changelist_view(request, extra_context=extra_context)
