from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.csrf import csrf_protect
import json
from django.contrib.contenttypes.models import ContentType
from django.apps import apps  # Add this import
from django.db import IntegrityError
from .serializers import get_dynamic_serializer, get_dynamic_update_data_serializer
from api.models import gov_department


# Helper function to parse and validate incoming JSON data
def parse_and_validate_data(request):
    try:
        data = json.loads(request.body)
        # print('18',data)
        plantid = data.get('treeID')
        pretablename = data.get('urlEnd')
        districtcode = int(data.get('distCode'))

        if not plantid or not pretablename:
            return None, None, districtcode, JsonResponse({'error': 'treeID and urlEnd are required fields'}, status=400)

        return plantid, pretablename, districtcode, None  # No error, return parsed values

    except json.JSONDecodeError:
        return None, None, districtcode, JsonResponse({'error': 'Invalid JSON payload'}, status=400)

# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
@csrf_protect
@login_required
def updateIndivisualPlant(request):
    if request.method not in ['POST', 'PATCH']:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    # Parse the data and validate common fields
    plantid, pretablename, distcode, error = parse_and_validate_data(request)
    if error:
        return error
    # maain----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    try:
        serializer_class = get_dynamic_serializer(f'CenterIndividualPlantation_{distcode}')
        # serializer_class = get_dynamic_serializer('CenterIndividualPlantation_119')
    except LookupError as e:
        #print( plantid, pretablename, distcode, error,"-------------")
        return JsonResponse({'error': f'Model CenterIndividualPlantation_{distcode} does not exist'}, status=400)

    
    # Handle the POST method
    if request.method == 'POST':
        return handle_post(request, serializer_class, plantid, pretablename, distcode)

    # Handle the PATCH method
    elif request.method == 'PATCH':
        return handle_patch(request, serializer_class, plantid, pretablename,distcode)
# ----------------------------------------------------------------------------------------------------------------------

def handle_post(request,serializer_class, plantid, pretablename,distcode):
    # print('162 post',serializer_class, plantid, pretablename, distcode)
    try:
        # Fetch the plant data for the given plantid and user
        user = request.user
        alivestatus = json.loads(request.body).get('alivestatus')
        newplantid = f"{pretablename}-{plantid}"
                
        existing_record = serializer_class.Meta.model.objects.filter(PLantid=newplantid).first()

        if existing_record:
            
            try:
                if existing_record.plant_alive_status:
                    # Update the existing record's plant_alive_status and other fields if necessary
                    existing_record.plant_alive_status = alivestatus
                    existing_record.any_update_status = True  # Example: mark as updated
                    existing_record.save()

                    #Return a response indicating the record was updated

                    return JsonResponse({
                        'message': f'Record for PLantid {existing_record.PLantid} updated successfully',
                        'existing': True,
                        'alivestatus':alivestatus,
                        'plantid':existing_record.PLantid,
                        'districtcode': existing_record.address_gp_id.District.District_id if existing_record.address_gp_id else distcode,
                        'lat':existing_record.latitude,
                        'lan':existing_record.longitude
                    }, status=200)

                    # return redirect('/update-phase/hi/aliveplant/')
                else:
                    # Return a response indicating the record was updated
                    return JsonResponse({
                        'message': f'Your plant with this id {newplantid} is already dead. Please plant a new plant.',
                        'existing': True,
                        'alivestatus':False,
                    }, status=200)
            except Exception as e:
                return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=500)


        # Dynamically resolve model class
        model_name = f"plantation_by{pretablename}"  # e.g., plantation_bypvt
        Model = apps.get_model(app_label='api', model_name=model_name)
        if not Model:
            return JsonResponse({'error': f'Model {model_name} does not exist'}, status=400)

        plants = Model.objects.filter(id=plantid, submitted_by=user.id)
        if not plants.exists():
            return JsonResponse({'error': f'No data found for plant_id {plantid}'}, status=404)

        plant = plants.first()

        new_plant_data = {
            'PLantid': newplantid,
            'plant_name': plant.plantation_name,
            'owner_name': None,
            'height': plant.plantation_height or 0.0,
            'latitude': round(plant.location_lat, 6) if plant.location_lat else 0.0,
            'longitude': round(plant.location_long, 6) if plant.location_long else 0.0,
            'address_gp_id': int(plant.gp_code.GP_FINAL_C) if plant.gp_code and plant.gp_code.GP_FINAL_C != '0' else None,
            'imageurl_1': plant.image1.url if plant.image1 else None,
            'imageurl_2': plant.image3.url if plant.image3 else None,
            'submitted_by_user_id': plant.submitted_by.id,
            'plant_alive_status': alivestatus,
            'status': True,
            'any_update_status': False,
            'created_at': plant.created_at,
        }

        if pretablename == 'gov':
            new_plant_data['submitted_by_department_id'] = plant.gov_department_id.id
            new_plant_data['land_ownership'] = plant.land_ownership.id
        elif pretablename == 'ngo':
            new_plant_data['submitted_by_ngo_name'] = plant.ngo_name or None
            new_plant_data['land_ownership'] = plant.land_ownership.id

        serializer = serializer_class(data=new_plant_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': f'Record for PLantid {newplantid} created successfully',
                'existing': False,
                'alivestatus': alivestatus,
                'plantid':newplantid,
                'districtcode':distcode,
                'lat': plant.location_lat,
                'long': plant.location_long,
            }, status=200)
        else:
            return JsonResponse({'error': serializer.errors}, status=400)

    except IntegrityError as e:
        return JsonResponse({'error': f'Database Integrity Error: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

def handle_patch(request, serializer_class, plantid, tablename, distcode):
    
    try:
        existing_record = serializer_class.Meta.model.objects.filter(PLantid=plantid).first()

        if existing_record:
            allowed_fields = ['submitted_by_department_id', 'owner_name', 'any_update_status', 'address_gp_id', 'latitude', 'longitude']
            filtered_data = {field: value for field, value in json.loads(request.body).items() if field in allowed_fields}

            # Update only the allowed fields using serializer
            serializer = serializer_class(existing_record, data=filtered_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({
                    'message': f'Record for PLantid {existing_record.PLantid} partially updated successfully',
                    'existing': True,
                    'updated_fields': filtered_data,
                }, status=200)
            else:
                #print('179 patch',serializer.errors)
                return JsonResponse({'error': serializer.errors}, status=400)
        else:
            return JsonResponse({
                'error': f'Record with PLantid {plantid} does not exist.',
            }, status=404)

    except IntegrityError as e:
        return JsonResponse({'error': f'Database Integrity Error: {str(e)}'}, status=500)

    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)

@csrf_protect
def plantgallery(request):
    district_code = request.GET.get('tbn')
    plantid = request.GET.get('pid')
    # Dynamically resolve model class
    model_center_name = f"CenterIndividualPlantation_{district_code}"
    model_update_name = f"UpdateData_{district_code}"

    try:
        # Get model class dynamically
        model_center_class = apps.get_model('update_app', model_center_name)
        model_update_class = apps.get_model('update_app', model_update_name)
        
        # Get plant data
        plant_data = model_center_class.objects.get(PLantid=plantid)
        update_data = model_update_class.objects.filter(center_entry_plant=plantid).order_by('-status_date_mmyyyy')
        
        #print(update_data,'view 200')
        
        context = {
            'pretablename': district_code,
            'plantid': plantid,
            'plant': plant_data,
            'update_data':update_data
        }
        
        return render(request, 'hi/plant_gallery.html', context)
        
    except LookupError:
        context = {
            'pretablename': district_code,
            'plantid': plantid, 
            'error': 'Invalid table name'
        }
        return render(request, 'hi/plant_gallery.html', context)
        
    except model_center_class.DoesNotExist:
        context = {
            'pretablename': district_code,
            'plantid': plantid,
            'error': 'Plant data not found'
        }
        return render(request, 'hi/plant_gallery.html', context)

@csrf_protect
@login_required
def updateAlivePlant(request):
    # Get tree ID and table name from request parameters
    tree_id = request.GET.get('treeID')
    District_code = int(request.GET.get('districtcode')) if request.GET.get('districtcode') else None
    model_update_name = f'UpdateData_{District_code}'
    locup = request.GET.get('locup')
    # print('272',f'UpdateData_{District_code}_',tree_id)
    # model_update_name = 'UpdateData_99'

    try:
        model_update_class = apps.get_model('update_app', model_update_name)
        serializer_update_class = get_dynamic_update_data_serializer(model_update_name)
    except LookupError as e:
        return JsonResponse({'error': f'Model {model_update_name} does not exist'}, status=404)

    # Handle the POST method
    if request.method == 'POST':
        user_id = request.user.id  # Get user ID from the request
        return UpdateAlive_handle_post(request, model_update_class, serializer_update_class, user_id)
    

    try:
        # Get model class dynamically
        model_center_name = f'CenterIndividualPlantation_{District_code}'
        # model_center_name = f'CenterIndividualPlantation_99'
        model_center_class = apps.get_model('update_app', model_center_name)
        
        # Get plant data filtered by ID
        plant_data = model_center_class.objects.get(PLantid=tree_id)
        departmentslist = gov_department.objects.all()

        #print("--------------",plant_data)
        qrcodehost = request.get_host()
        context = {
            'tree_id': tree_id,
            'District_code': District_code,
            'plant': plant_data,
            'departmentslist': departmentslist,
            'qrcodeurl':f"{qrcodehost}/geotree/?qr={District_code}-{tree_id}"
        }
        if locup:
            return render(request, 'hi/updateAlivePlantWithLocation.html', context)
        return render(request, 'hi/updateAlivePlantWithoutLocation.html', context)
    except (LookupError, model_center_class.DoesNotExist):
        context = {
            'tree_id': tree_id,
            'District_code': District_code,
            'error': 'Plant data not found'
        }
        if locup:
            return render(request, 'hi/updateAlivePlantWithLocation.html', context)
        return render(request, 'hi/updateAlivePlantWithoutLocation.html', context)

def UpdateAlive_handle_post(request, model_update_class, serializer_update_class, user_id):
    try:
        # Use request.POST and request.FILES since FormData is used in the frontend
        data = request.POST.dict()  # Convert POST data to a dictionary
        files = request.FILES  # File data

        # Add file to the data dictionary
        data['Update_image1'] = files.get('Update_image1')
        data['user'] = user_id

        serializer = serializer_update_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({
                'message': f'Record for PlantID {serializer.validated_data["center_entry_plant"]} updated successfully',
            }, status=200)
        else:
            # Return formatted errors
            errors = serializer.errors
            formatted_errors = {
                field: ", ".join(messages) for field, messages in errors.items()
            }
            return JsonResponse({
                'error': 'Validation failed',
                'details': formatted_errors
            }, status=400)
    except Exception as e:
        #print('Error processing the request:', e)
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)



@csrf_protect
def mapValidation(request):
    # Get tree ID and table name from request parameters
    tree_id = request.GET.get('treeID')
    District_code = request.GET.get('districtcode')

    # Validate required parameters
    if not tree_id or not District_code:
        context = {
            'error': 'Missing required parameters: tree ID and district code'
        }
        return render(request, 'hi/map-location.html', context)

    try:
        # Get model class dynamically
        model_name = f'UpdateData_{District_code}'
        # model_name = f'UpdateData_119'
        model_class = apps.get_model('update_app', model_name)

        last_update_details = (
            model_class.objects.filter(center_entry_plant=tree_id)
            .order_by('-status_date_mmyyyy')
            .values_list('status_date_mmyyyy', flat=True)
            .first()
        )
        #print(last_update_details,"last details 260 view")
        context = {
            'tree_id': tree_id,
            'District_code': District_code,
            'last_update_details': last_update_details,
        }
        return render(request, 'hi/map-location.html', context)
        
    except (LookupError):
        context = {
            'tree_id': tree_id,
            'District_code': District_code,
            'error': 'Plant data not found'
        }
        return render(request, 'hi/map-location.html', context)

from portaldash.models import DistrictList
    
@csrf_protect
@login_required
def updateDistrict(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)
            plantation_id = data.get("plantation_id")
            district_id = data.get("district_id")
            table_name = data.get("table_name")
            
            # Ensure all required parameters are provided
            if not plantation_id or not district_id or not table_name:
                return JsonResponse({"error": "Plantation ID, District ID, and Table Name are required."}, status=400)
            
            # Dynamically resolve model class
            model_name = f"plantation_by{table_name}"  # e.g., plantation_bypvt
            model_class = apps.get_model(app_label='api', model_name=model_name)
            if not model_class:
                return JsonResponse({'error': f'Model {model_name} does not exist'}, status=400)

            # Retrieve the plantation instance
            plantation = get_object_or_404(model_class, id=plantation_id)
            
            # Check if the logged-in user is the one who submitted the record
            if plantation.submitted_by != request.user:
                return JsonResponse({"error": "You are not authorized to update this record."}, status=403)
            
            # Retrieve the new district instance
            new_district = get_object_or_404(DistrictList, DISTRICT_C=district_id)
            
            # Update the dict_code field
            plantation.dict_code = new_district
            plantation.save()
            
            return JsonResponse({
                "message": f"Plantation {plantation_id} updated successfully.",
                "updated_district": new_district.DISTRICT_N
            })
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    pid = request.GET.get('pid')
    tbn = request.GET.get('tbn')

    # print(tbn,pid,"400")
    district_list = DistrictList.objects.all()
    context = {
        'district_list': district_list,
        'table_name':tbn,
        'plant_id':pid
    }
    return render(request, './hi/update-district-previous.html', context)