from django.urls import reverse
from django.shortcuts import render, redirect ,get_object_or_404
from django.http import HttpResponse , JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from account.models import TempUser, User, UserDistrictPermissions
import datetime
import time
from django.views import View
from django.utils.decorators import method_decorator
from api.models import *
from django.utils.crypto import get_random_string
import requests
from django.core.serializers import serialize
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.template.loader import render_to_string
from .decorators import staff_required
import json

@login_required
@csrf_protect
@staff_required
def certificate_adm(request):
    # user = request.user
    # certidata = TempStorageCertificateInfo.objects.all()
    # paginator = Paginator(certidata, 10)
    # page_number = request.GET.get('page')
    # cert_info = paginator.get_page(page_number)
    # # certificate_data = serialize('json', certidata)
    # return render(request, 'certificateAdm/certificateAdm.html', {'cert_info': cert_info, 'user': user})

    user = request.user
    certidata =TempStorageCertificateInfo.objects.all().order_by('-created_at')
    
    # Fetch rows per page from request, defaulting to 10
    rows_per_page = int(request.GET.get('rows', 10))
    paginator = Paginator(certidata, rows_per_page)
    
    page_number = request.GET.get('page')
    skip_to_page = request.GET.get('skip_to_page')  # Get the page number to skip to
    
    # Handle skip to page functionality
    if skip_to_page:
        try:
            cert_info = paginator.page(skip_to_page)
        except (PageNotAnInteger, EmptyPage):
            cert_info = paginator.page(1)  # Fallback to first page if invalid page number
    else:
        cert_info = paginator.get_page(page_number)
    
    # Handle selected rows (assuming you've stored them in session as shown earlier)
    selected_rows = request.session.get('selected_rows', [])
    
    if request.method == 'POST':
        # Handle row selection form submission
        selected_rows = request.POST.getlist('selected_rows', [])
        request.session['selected_rows'] = selected_rows
    
    # Debugging prints for verification
    print(f"Rows per page: {rows_per_page}, Page number: {page_number}")
    print(f"cert info object: {cert_info}")
    print(f"Selected rows: {selected_rows}")
    
    # Render template with paginated data, selected rows, and user info
    return render(request, 'certificateAdm/certificateAdm.html', {
        'cert_info': cert_info,
        'rows_per_page': rows_per_page,
        'user': user,
        'selected_rows': selected_rows,
    })



from PIL import Image, ImageDraw, ImageFont
def generate_certificate(template_path, name, selfie_path, certificate_number, output_path):
    start_time = time.time()  # Start timing the process
    # Load the certificate template
    template = Image.open(template_path)
    # Load the selfie image
    selfie = Image.open(selfie_path).resize((280, 365))  # Adjust the size as needed
    # Create a draw object
    draw = ImageDraw.Draw(template)

    # Define font and size
    font1_path = os.path.join(settings.BASE_DIR, 'private/certificates/AnastasiaScript.ttf')  # Ensure the path is correct
    font1 = ImageFont.truetype(font1_path, 40)# Adjust font size as needed
    # Define font and size
    font = ImageFont.truetype("arial.ttf", 40)  # Adjust font size as needed
    # Get the current date

    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    # Define the section coordinates
    x_start, y_start = 850, 582
    x_end = 1230
    
    # Calculate the width of the section
    section_width = x_end - x_start
    
    # Calculate the bounding box of the first text
    text1_bbox = draw.textbbox((0, 0), name, font=font1)
    text1_width = text1_bbox[2] - text1_bbox[0]
    text1_height = text1_bbox[3] - text1_bbox[1]
    
    # Calculate the position to center the first text within the section
    centered_x = x_start + (section_width - text1_width) // 2
    name_position = (centered_x, y_start)


    # Define positions (adjust these positions based on your template)
    # name_position = (200, 200)
    date_position = (1730, 1193)
    certificate_number_position = (356, 1193)
    selfie_position = (170, 398)
    # Add text to the template
    draw.text(name_position, name, font=font1, fill="black")
    draw.text(date_position, current_date, font=font, fill="black")
    draw.text(certificate_number_position, certificate_number, font=font, fill="black")
    # Paste the selfie image onto the template
    template.paste(selfie, selfie_position)
    # Save the certificate
    template.save(output_path)
    end_time = time.time()  # End timing the process
    processing_time = end_time - start_time

    # print(f"Certificate generated successfully and saved to {output_path}")
    # print(f"Processing time: {processing_time:.2f} seconds")


@login_required
@csrf_protect
@staff_required
def approve_certificate(request):
    if request.method == 'POST':
        cert_ids = request.POST.getlist('ids[]')  # Get list of certificate IDs
        results = {'success': [], 'failed': []}

        for cert_id in cert_ids:
            try:
                certificate = get_object_or_404(TempStorageCertificateInfo, certificate_id=cert_id)
                # Define paths
                template_path = os.path.join(settings.BASE_DIR, 'private/certificates/c2.webp')
                selfie_path = certificate.selfi_image.path
                output_path = os.path.join(settings.MEDIA_ROOT, f'images/certificate_image/{certificate.certificate_id}_certificate.png')

                # Generate the certificate
                generate_certificate(template_path, certificate.certificate_holder_name, selfie_path, certificate.certificate_id, output_path)

                # Save the generated certificate to CertificateStorage
                cert_storage = CertificateStorage(
                    certificate_id=certificate.certificate_id,
                    user_id=certificate.user_id,
                    certificate_image=f'images/certificate_image/{certificate.certificate_id}_certificate.png'
                )
                cert_storage.save()

                results['success'].append(cert_id)
            except Exception as e:
                results['failed'].append({'id': cert_id, 'error': str(e)})

        return JsonResponse(results)
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



@login_required
@csrf_protect
@staff_required
def delete_certificate(request):
    cert_id = request.POST.get('id')
    if not cert_id:
        return JsonResponse({'success': False, 'error': 'Certificate ID not provided'})
    try:
        certificate = get_object_or_404(TempStorageCertificateInfo, certificate_id=cert_id)
        certificate.delete()
        return JsonResponse({'success': True})
    except TempStorageCertificateInfo.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Certificate not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@csrf_protect
def login_adm(request):
    if request.method == 'POST':
        userid = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=userid, password=password)
        if user is not None:
            if user.is_staff:
                auth_login(request, user)
                return redirect('dashboardadm')
                # return render(request, 'dashboard/dashboard.html', {'user': user})
            else:
                return render(request, 'loginadm/loginadm.html', {'error': 'Permission denied'})
        else:
            return render(request, 'loginadm/loginadm.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'loginadm/loginadm.html')  # Render the initial login form

        
@login_required
def logout_viewadm(request):
    auth_logout(request)
    return render(request, 'loginadm/loginadm.html')



@csrf_protect
def reg_adm(request):
    role = registration_role_department.objects.order_by('reg_dep_name')

    dept = gov_department.objects.order_by('department_name')
    
    return render(request, 'regadm/kegadm.html', {'role': role, 'dept':dept})


from portaldash.models import ShortDatabase_normal

@login_required
@staff_required
@require_POST
def download_kmz(request):
    try:
        # Parse the request body
        data = json.loads(request.body)
        section2 = data.get('section2', [])
        blocks = data.get('blocks', [])
        # print(section2,"--------------------------------")
        # Ensure that at least one checkbox in each section was selected
        if not section2 or not blocks:
            return JsonResponse({'error': 'Please select at least one option in both sections.'}, status=400)
        if section2[0] == '1':
            # Filter records
            filtered_records = plantation_bypvt.objects.filter(block_code__BLOCK_C__in=blocks)

            # Convert queryset to a list of dictionaries including specific fields
            filtered_records_data = list(filtered_records.values(
                'id',
                'plantation_name',
                'plantation_height',
                'location_lat',
                'location_long',
                'created_at'
            ))

        if section2[0] == '2':
            # Filter records
            filtered_records = plantation_bygov.objects.filter(block_code__BLOCK_C__in=blocks)

            # Convert queryset to a list of dictionaries including specific fields
            filtered_records_data = list(filtered_records.values(
                'id',
                'plantation_name',
                'gov_department_id__department_name',
                'land_ownership__land_ownership',
                'plantation_height',
                'location_lat',
                'location_long',
                'created_at'
            ))
        
        if section2[0] == '3':
            # Filter records
            filtered_records = plantation_byngo.objects.filter(block_code__BLOCK_C__in=blocks)

            # Convert queryset to a list of dictionaries including specific fields
            filtered_records_data = list(filtered_records.values(
                'id',
                'plantation_name',
                'ngo_name',
                'land_ownership__land_ownership',
                'plantation_height',
                'location_lat',
                'location_long',
                'created_at'
            ))
        
        if section2[0] == '4':
            # Filter records
            filtered_records = BlockPlantation.objects.filter(block_code__BLOCK_C__in=blocks)
            
            # Convert queryset to a list of dictionaries including specific fields
            filtered_records_data = list(filtered_records.values(
                'id',
                'planta_name_text',
                'number_of_plants',
                'plantationArea',
                'goverment_departmet__department_name',
                'land_ownership',
                'location_list',
                'location_lat',
                'location_long',
                'created_at'
            ))
            # print(filtered_records_data)

        # Return a success response with the serialized data
        return JsonResponse({'filtered_records': filtered_records_data,'selectedsection':section2[0]}, status=200, safe=False)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



import re
@login_required
@csrf_protect
@staff_required
def dashboard_adm(request):
    user = request.user
    
    # Get the districts that the user has permission for
    user_districts = UserDistrictPermissions.objects.filter(user=user, status=True).select_related('district')
    
     # Initialize the variable with a default value
    sub_view_content_download_kmz = ""
    # Extract the district name and code
    districts = [{'DISTRICT_N': permission.district.DISTRICT_N, 'DISTRICT_C': permission.district.DISTRICT_C} for permission in user_districts]  
    if districts:
       # Assuming you want to filter blocks by the first district code in the lis

        # Extract only the numeric characters from the DISTRICT_C field
        first_district_code = re.sub(r'\D', '', districts[0]['DISTRICT_C'])
        # print(first_district_code, 'first_district_code', type(first_district_code), first_district_code == '119')
        blocks = ShortDatabase_normal.objects.filter(DISTRICT_C=first_district_code).values('BLOCK_N', 'BLOCK_C').distinct('BLOCK_C')
        # Render sub view template as a string
        sub_view_content_download_kmz = render_to_string('components/download_kmz/index.html', {'sub_data': blocks, 'first_block': districts[0]}, request=request)
    
    # Pass the rendered content to the main view's context
    context = {
        'user': user,
        'sub_view_content_download_kmz': sub_view_content_download_kmz,
    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required
@csrf_protect
@staff_required
def plantationdata_pvt_adm(request):
    user = request.user
    pvtdata = plantation_bypvt.objects.all().order_by('-created_at')
    
    # Fetch rows per page from request, defaulting to 10
    rows_per_page = int(request.GET.get('rows', 10))
    paginator = Paginator(pvtdata, rows_per_page)
    
    page_number = request.GET.get('page')
    skip_to_page = request.GET.get('skip_to_page')  # Get the page number to skip to
    
    # Handle skip to page functionality
    if skip_to_page:
        try:
            pvt_info = paginator.page(skip_to_page)
        except (PageNotAnInteger, EmptyPage):
            pvt_info = paginator.page(1)  # Fallback to first page if invalid page number
    else:
        pvt_info = paginator.get_page(page_number)
    
    # Handle selected rows (assuming you've stored them in session as shown earlier)
    selected_rows = request.session.get('selected_rows', [])
    
    if request.method == 'POST':
        # Handle row selection form submission
        selected_rows = request.POST.getlist('selected_rows', [])
        request.session['selected_rows'] = selected_rows
    
    # Debugging prints for verification
    # print(f"Rows per page: {rows_per_page}, Page number: {page_number}")
    # print(f"Pvt info object: {pvt_info}")
    # print(f"Selected rows: {selected_rows}")
    
    # Render template with paginated data, selected rows, and user info
    return render(request, 'plantdataAdm/plantdataAdmpvt.html', {
        'pvt_info': pvt_info,
        'rows_per_page': rows_per_page,
        'user': user,
        'selected_rows': selected_rows,
    })



@login_required
@csrf_protect
@staff_required
def plantationdata_gov_adm(request):
    user = request.user
    govdata = plantation_bygov.objects.all().order_by('-created_at')
    
    # Fetch rows per page from request, defaulting to 10
    rows_per_page = int(request.GET.get('rows', 10))
    paginator = Paginator(govdata, rows_per_page)
    
    page_number = request.GET.get('page')
    skip_to_page = request.GET.get('skip_to_page')  # Get the page number to skip to
    
    # Handle skip to page functionality
    if skip_to_page:
        try:
            gov_info = paginator.page(skip_to_page)
        except (PageNotAnInteger, EmptyPage):
            gov_info = paginator.page(1)  # Fallback to first page if invalid page number
    else:
        gov_info = paginator.get_page(page_number)
    
    # Handle selected rows (assuming you've stored them in session as shown earlier)
    selected_rows = request.session.get('selected_rows', [])
    
    if request.method == 'POST':
        # Handle row selection form submission
        selected_rows = request.POST.getlist('selected_rows', [])
        request.session['selected_rows'] = selected_rows
    
    # Debugging prints for verification
    # print(f"Rows per page: {rows_per_page}, Page number: {page_number}")
    # print(f"gov info object: {gov_info}")
    # print(f"Selected rows: {selected_rows}")
    
    # Render template with paginated data, selected rows, and user info
    return render(request, 'plantdataAdm/plantdataAdmgov.html', {
        'gov_info': gov_info,
        'rows_per_page': rows_per_page,
        'user': user,
        'selected_rows': selected_rows,
    })


@login_required
@csrf_protect
@staff_required
def plantationdata_ngo_adm(request):
    user = request.user
    ngodata = plantation_byngo.objects.all().order_by('-created_at')
    
    # Fetch rows per page from request, defaulting to 10
    rows_per_page = int(request.GET.get('rows', 10))
    paginator = Paginator(ngodata, rows_per_page)
    
    page_number = request.GET.get('page')
    skip_to_page = request.GET.get('skip_to_page')  # Get the page number to skip to
    
    # Handle skip to page functionality
    if skip_to_page:
        try:
            ngo_info = paginator.page(skip_to_page)
        except (PageNotAnInteger, EmptyPage):
            ngo_info = paginator.page(1)  # Fallback to first page if invalid page number
    else:
        ngo_info = paginator.get_page(page_number)
    
    # Handle selected rows (assuming you've stored them in session as shown earlier)
    selected_rows = request.session.get('selected_rows', [])
    
    if request.method == 'POST':
        # Handle row selection form submission
        selected_rows = request.POST.getlist('selected_rows', [])
        request.session['selected_rows'] = selected_rows
    
    # Debugging prints for verification
    # print(f"Rows per page: {rows_per_page}, Page number: {page_number}")
    # print(f"ngo info object: {ngo_info}")
    # print(f"Selected rows: {selected_rows}")
    
    # Render template with paginated data, selected rows, and user info
    return render(request, 'plantdataAdm/plantdataAdmngo.html', {
        'ngo_info': ngo_info,
        'rows_per_page': rows_per_page,
        'user': user,
        'selected_rows': selected_rows,
    })


import pandas as pd
from datetime import datetime

@login_required
@csrf_protect
@staff_required
def download_plantation_csv(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    table_name = request.GET.get('plantation_ownership_table')

    # Validate start and end dates
    if not start_date_str or not end_date_str:
        return HttpResponse('Invalid date range', status=400)

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    except ValueError:
        return HttpResponse('Invalid date format', status=400)

    # Ensure end_date is not earlier than start_date
    if end_date < start_date:
        return HttpResponse('End date cannot be earlier than start date', status=400)

    if table_name == 'plantation_bygov':

        # Fetch data from the plantation_bygov table based on the date range
        plantations_qs = plantation_bygov.objects.filter(created_at__range=(start_date, end_date)).select_related('gov_department_id_id')

        # Define fields to fetch in the desired order
        fields = [
            'id', 'plantation_name', 'plantation_height', 'gov_department_id_id__department_name', 
            'land_ownership_id__land_ownership', 'location_lat', 'location_long', 
            'submitted_by__phone', 'status', 'created_at', 'updated_at'
        ]

    elif table_name == 'plantation_byngo':
        print('Fetching data from')

        #Fetch data from the plantation_bygov table based on the date range
        plantations_qs = plantation_byngo.objects.filter(created_at__range=(start_date, end_date)).select_related('land_ownership_byngo')

        # Define fields to fetch in the desired order
        fields = [
            'id', 'plantation_name', 'plantation_height', 'ngo_name', 
            'land_ownership_id__land_ownership', 'location_lat', 'location_long', 
            'submitted_by__phone', 'status', 'created_at', 'updated_at'
        ]

    elif table_name == 'plantation_bypvt':
        #Fetch data from the plantation_bygov table based on the date range
        plantations_qs = plantation_bypvt.objects.filter(created_at__range=(start_date, end_date))

        # Define fields to fetch in the desired order
        fields = [
            'id', 'plantation_name', 'plantation_height',
            'location_lat', 'location_long',
            'submitted_by__phone', 'status', 'created_at', 'updated_at'
        ]


    else:
        return HttpResponse('Table name error', status=400)

    # Fetch values_list with named fields
    plantations_values = plantations_qs.values_list(*fields)

    # Convert QuerySet to DataFrame
    df = pd.DataFrame.from_records(plantations_values, columns=fields)

    # Convert DataFrame to CSV
    csv_buffer = df.to_csv(index=False)

    # Create HTTP response with CSV content
    response = HttpResponse(csv_buffer, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=plantation_data.csv'
    return response




from django.db import connection, transaction
from django.http import JsonResponse
from admindashboard.decorators import staff_required
from django.contrib.auth.decorators import login_required, permission_required
@login_required
@csrf_protect
@staff_required
def execute_sql(request):
    try:
        # Start a transaction block
        with transaction.atomic():
            # First query to update Total_block_plantation_Non_Verify_C
            with connection.cursor() as cursor:
                cursor.execute("""
                    WITH TotalCounts AS (
                        SELECT gp_code_id, SUM(CAST(number_of_plants AS int)) AS total_sum
                        FROM api_blockplantation
                        GROUP BY gp_code_id
                    )
                    UPDATE portaldash_shortdatabase_normal
                    SET "Total_block_plantation_Non_Verify_C" = tc.total_sum
                    FROM TotalCounts tc
                    WHERE portaldash_shortdatabase_normal."GP_FINAL_C" = tc.gp_code_id;
                """)

            # Second query to update Total_Tag_Tree_Non_Verify_C
            with connection.cursor() as cursor:
                cursor.execute("""
                    WITH TotalCounts AS (
                        SELECT
                            gp_code_id,
                            COUNT(*) AS total_count
                        FROM (
                            SELECT gp_code_id FROM api_plantation_bygov
                            UNION ALL
                            SELECT gp_code_id FROM api_plantation_bypvt
                            UNION ALL
                            SELECT gp_code_id FROM api_plantation_byngo
                        ) AS combined_tables
                        GROUP BY gp_code_id
                    )
                    UPDATE portaldash_shortdatabase_normal
                    SET "Total_Tag_Tree_Non_Verify_C" = tc.total_count
                    FROM TotalCounts tc
                    WHERE portaldash_shortdatabase_normal."GP_FINAL_C" = tc.gp_code_id;
                """)

        # Commit the transaction if everything is successful
        return JsonResponse({"status": "success", "message": "Database updated successfully!"})
    
    except Exception as e:
        #logger.error("Error executing SQL: %s", str(e))
        return JsonResponse({"status": "error", "message": str(e)})
