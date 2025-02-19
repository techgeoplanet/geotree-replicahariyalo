from django.shortcuts import render
import requests
from django.conf import settings

# Create your views here.
def mapcontent(request):
    lat = request.GET.get('lat', 25)
    long = request.GET.get('long', 74)
    return render(request, 'map_web/map_web.html', {'lat': lat, 'long': long})


def mappolygon(request):
    polygon = request.GET.get('polygon', None)  # Retrieve the 'polygon' parameter from the URL
    context = {
        'polygon': polygon
    }
    return render(request, 'map_polygon/map_polygon.html', context)


from django.http import JsonResponse

def GetCurrentLoactionAddresh(request):
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    # print(settings.GEO_MAP_API_URL, settings.GEO_MAP_API_X_AUTH_KEY, settings.GEO_MAP_API_X_USERNAME)
    try:
        if lat and lon:
            url = f"{settings.GEO_MAP_API_URL}?lat={lat}&lon={lon}"

            headers = {
                'X-Auth-Key': settings.GEO_MAP_API_X_AUTH_KEY,
                'X-Username': settings.GEO_MAP_API_X_USERNAME
            }

            response = requests.get(url, headers=headers)
            data = response.json()  # Convert the response to JSON
        # Add lat and lon to the response data
            data.update({'lat': lat, 'lon': lon})
        else:
            data = {'error': 'Latitude and Longitude are required'}
        
    except requests.exceptions.RequestException as e:
        # Handle any exceptions that occur during the API request
        data = {'error': str(e), 'lat': lat, 'lon': lon}

    # Return the data as JSON
    return JsonResponse(data)