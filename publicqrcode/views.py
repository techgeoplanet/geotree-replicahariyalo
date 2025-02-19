from django.shortcuts import render
from django.http import HttpRequest
from .models import QrcodeVisiter

def qrid_view(request: HttpRequest):
    # Get the id from the request GET parameters
    id = request.GET.get('id')

    try:
        if id: 
            # Create a new entry every time, even if the same qrcode exists
            visitor = QrcodeVisiter.objects.create(qrcode=id)
    except Exception as e:
        print(f"An error occurred: {e}")

    # Get the total count of visitors in the database
    total_count = QrcodeVisiter.objects.count()

    # Render an HTML page with the total count
    return render(request, 'qrid_page.html', {"total_count": total_count,"qrid":id})
