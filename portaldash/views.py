from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from django.http import JsonResponse
import time
from django.views import View
from django.utils.decorators import method_decorator
from api.models import *
from django.utils.crypto import get_random_string
import requests
from api.middleware import RequestLimitMiddleware
from .models import *
from django.db.models import Sum, IntegerField
from django.db.models.functions import Cast

from api.models import BlockPlantation, plantation_bygov

from django.db.models import Sum, IntegerField,F
from django.db.models.functions import Cast
from django.db.models import Count

@csrf_protect
def portalmap_view(request):
    return render(request, 'portal_map.html')


import json
@csrf_protect
def portaldash_view(request):
    try:
        # Fetch or create a SiteVisitCount object
        # Ensure there's only one record or adapt accordingly
        site_visit, created = SiteVisitCount.objects.get_or_create(id=1)
        
        # Increment the site visit count using F() expressions
        SiteVisitCount.objects.filter(id=site_visit.id).update(SiteVisitCount=F('SiteVisitCount') + 1)
    except Exception as e:
        # Log the error or handle it as needed
        print(f"Error updating site visit count: {e}")
        site_visit = None

    aggregated_data = ShortDatabase_normal.objects.values('DISTRICT_C', 'DISTRICT_N').annotate(
        total_tag_tree_verify=Sum(Cast('Total_Tag_Tree_Verify_C', output_field=IntegerField())),
        total_tag_tree_non_verify=Sum(Cast('Total_Tag_Tree_Non_Verify_C', output_field=IntegerField())),
        total_block_plantation_verify=Sum(Cast('Total_block_plantation_Verify_C', output_field=IntegerField())),
        total_block_plantation_non_verify=Sum(Cast('Total_block_plantation_Non_Verify_C', output_field=IntegerField())),
    ).order_by('DISTRICT_C')

    aggregated_data_list = list(aggregated_data)

    Chartdata = ShortDatabase_chart.objects.all()
    DepartmentList = gov_department.objects.all()
    # Fetch the single object
    TotalPlantations = TotalNumberOfPlantations.objects.first()

    # SiteVisit = SiteVisitCount.objects.first()

    TotalNumberOfInputsInBlockPlantations = BlockPlantation.objects.count()


    context = {
        'number_of_species': 250,
        'number_of_blockplantation_inputs': TotalNumberOfInputsInBlockPlantations,
        'aggregated_data_list': json.dumps(aggregated_data_list),
        'Chartdata': Chartdata,
        'DepartmentList': DepartmentList,
        'SiteVisit': site_visit.SiteVisitCount if site_visit else 0,  # Handle None case
        'TotalPlantations': TotalPlantations.TotalPlantations if TotalPlantations else 0,  # Handle None case
    }

    return render(request, 'portal_dash.html', context)


@csrf_protect
def departmentdata_dash_view(request):
    # Get the 'dep' query parameter from the request
    department = request.GET.get('dep')
    department_name = request.GET.get('depName')
    
    if department:
        # Query to get the total number of plants per district where goverment_departmet = 1
        plants_per_district = BlockPlantation.objects.filter(goverment_departmet=department).filter(
        number_of_plants__regex=r'^\d+$'  # Only include numeric values
        ).values('dict_code__DISTRICT_N').annotate(
            total_plants=Sum(Cast('number_of_plants', IntegerField()))
        )
        # # # Example of accessing the results
        # for item in plants_per_district:
        #     print(f"District: {item['dict_code__DISTRICT_N']}, Total Plants: {item['total_plants']}")

        # Query to count repeated rows by dict_code where gov_department_id = 1
        repeated_rows_per_district = plantation_bygov.objects.filter(
            gov_department_id=department
        ).values('dict_code__DISTRICT_N').annotate(
            count=Count('id')
        ).order_by('-count')
        # # Example of accessing the results
        # for item in repeated_rows_per_district:
        #     viewcount+=item['count']
        #     print(f"District: {item['dict_code__DISTRICT_N']}, Count: {item['count']}")

        # Convert to lists of dictionaries for JSON serialization
        block_plantation_list = list(plants_per_district)
        indivisual_plantation_list = list(repeated_rows_per_district)

        # print(block_plantation_list,indivisual_plantation_list)

        # Serialize the data to JSON
        block_plantation_data = json.dumps(block_plantation_list)
        indivisual_plantation_data = json.dumps(indivisual_plantation_list)
        department_name = json.dumps(department_name)

        context = {
            'block_plantation_data': block_plantation_data,
            'indivisual_plantation_data': indivisual_plantation_data,
            'department_name': department_name
        }

        
        # Process the department data as needed
        # For example, you could render a template or return a response
        return render(request, 'departmentdata/department_dash_excel.html', context)
    else:
        return HttpResponse("No department specified.")


@csrf_protect
def portalblockmap_view(request):  
    return render(request, 'portal_blockmap.html')

@csrf_protect
def portalblock_view(request, id):
    # Filter aggregated_data based on the id parameter matching the BLOCK_N field
    aggregated_data = ShortDatabase_normal.objects.values('BLOCK_C', 'BLOCK_N').annotate(
        total_tag_tree_verify=Sum(Cast('Total_Tag_Tree_Verify_C', output_field=IntegerField())),
        total_tag_tree_non_verify=Sum(Cast('Total_Tag_Tree_Non_Verify_C', output_field=IntegerField())),
        total_block_plantation_verify=Sum(Cast('Total_block_plantation_Verify_C', output_field=IntegerField())),
        total_block_plantation_non_verify=Sum(Cast('Total_block_plantation_Non_Verify_C', output_field=IntegerField())),
    ).filter(DISTRICT_C=id).order_by('BLOCK_C')  # Add filter for BLOCK_N

    site_visit, created = SiteVisitCount.objects.get_or_create(id=1)
    
    # Increment the site visit count using F() expressions
    SiteVisitCount.objects.filter(id=site_visit.id).update(SiteVisitCount=F('SiteVisitCount') + 1)



    aggregated_data_list = list(aggregated_data)
    # print(aggregated_data_list)
    DISTRICT_N_DATA = 'null'

    try:
        district = DistrictList.objects.get(DISTRICT_C=id)
        DISTRICT_N_DATA = district.DISTRICT_N
    except DistrictList.DoesNotExist:
         DISTRICT_N_DATA = 'none'

    TotalNumberOfInputsInBlockPlantations = BlockPlantation.objects.filter(dict_code=id).count()
    DepartmentList = gov_department.objects.all()
    context = {
        'number_of_species':250,
        'aggregated_data_list': json.dumps(aggregated_data_list),
        'DISTRICT_C': id,
        'DISTRICT_N_DATA':DISTRICT_N_DATA,
        'TotalNumberOfInputsInBlockPlantations':TotalNumberOfInputsInBlockPlantations,
        'DepartmentList':DepartmentList,
        'SiteVisit': site_visit.SiteVisitCount if site_visit else 0,  # Handle None case

    }

    return render(request, 'portal_block.html', context)


@csrf_protect
def departmentdata_block_view(request):
    # Get the 'dep' query parameter from the request
    distid = request.GET.get('distid')
    distname = request.GET.get('distname')
    department = request.GET.get('dep')
    department_name = request.GET.get('depName')
    
    if department:
        # Query to get the total number of plants per district where goverment_departmet = 1
        plants_per_district = BlockPlantation.objects.filter(goverment_departmet=department,dict_code=distid).filter(
        number_of_plants__regex=r'^\d+$'  # Only include numeric values
        ).values('block_code__BLOCK_N').annotate(
            total_plants=Sum(Cast('number_of_plants', IntegerField()))
        )
        # # # Example of accessing the results
        # for item in plants_per_district:
        #     print(f"District: {item['dict_code__DISTRICT_N']}, Total Plants: {item['total_plants']}")

        # Query to count repeated rows by dict_code where gov_department_id = 1
        repeated_rows_per_district = plantation_bygov.objects.filter(
            gov_department_id=department,dict_code=distid
        ).values('block_code__BLOCK_N').annotate(
            count=Count('id')
        ).order_by('-count')
        # # Example of accessing the results
        # for item in repeated_rows_per_district:
        #     viewcount+=item['count']
        #     print(f"District: {item['dict_code__DISTRICT_N']}, Count: {item['count']}")

        # Convert to lists of dictionaries for JSON serialization
        block_plantation_list = list(plants_per_district)
        indivisual_plantation_list = list(repeated_rows_per_district)

        # print(block_plantation_list,indivisual_plantation_list)

        # Serialize the data to JSON
        block_plantation_data = json.dumps(block_plantation_list)
        indivisual_plantation_data = json.dumps(indivisual_plantation_list)
        department_name = json.dumps(department_name)
        distname = json.dumps(distname)

        context = {
            'block_plantation_data': block_plantation_data,
            'indivisual_plantation_data': indivisual_plantation_data,
            'department_name': department_name,
            'distname': distname,
        }
        # Process the department data as needed
        # For example, you could render a template or return a response
        return render(request, 'departmentdata/department_block_excel.html', context)
    else:
        return HttpResponse("No department specified.")



@csrf_protect
def portalgpmap_view(request):
    return render(request, 'portal_gpmap.html')

@csrf_protect
def portalgp_view(request ,id):

    site_visit, created = SiteVisitCount.objects.get_or_create(id=1)
    
    # Increment the site visit count using F() expressions
    SiteVisitCount.objects.filter(id=site_visit.id).update(SiteVisitCount=F('SiteVisitCount') + 1)


    # Filter aggregated_data based on the id parameter matching the BLOCK_N field
    aggregated_data = ShortDatabase_normal.objects.values('GP_FINAL_C', 'GP_FINAL_N').annotate(
        total_tag_tree_verify=Sum(Cast('Total_Tag_Tree_Verify_C', output_field=IntegerField())),
        total_tag_tree_non_verify=Sum(Cast('Total_Tag_Tree_Non_Verify_C', output_field=IntegerField())),
        total_block_plantation_verify=Sum(Cast('Total_block_plantation_Verify_C', output_field=IntegerField())),
        total_block_plantation_non_verify=Sum(Cast('Total_block_plantation_Non_Verify_C', output_field=IntegerField())),
    ).filter(BLOCK_C=id).order_by('GP_FINAL_N')  # Add filter for BLOCK_N

    aggregated_data_list = list(aggregated_data)
    # print(aggregated_data_list)
     # # print(aggregated_data_list)
    BLOCK_N_DATA = 'null'

    try:
        Block = BlockList.objects.get(BLOCK_C=id)
        BLOCK_N_DATA = Block.BLOCK_N
    except DistrictList.DoesNotExist:
        BLOCK_N_DATA = 'none'

    TotalNumberOfInputsInBlockPlantations = BlockPlantation.objects.filter(block_code=id).count()
    DepartmentList = gov_department.objects.all()

    context = {
        'number_of_species':250,
        'aggregated_data_list': json.dumps(aggregated_data_list),
        'BLOCK_C': id,
        'BLOCK_N_DATA':BLOCK_N_DATA,
        'TotalNumberOfInputsInBlockPlantations':TotalNumberOfInputsInBlockPlantations,
        'DepartmentList':DepartmentList,
        'SiteVisit': site_visit.SiteVisitCount if site_visit else 0,  # Handle None case   
    }
    return render(request, 'portal_gp.html', context)



@csrf_protect
def departmentdata_gp_view(request):
    # Get the 'dep' query parameter from the request
    blockid = request.GET.get('blockid')
    blockname = request.GET.get('blockname')
    department = request.GET.get('dep')
    department_name = request.GET.get('depName')
    
    if department:
        # Query to get the total number of plants per district where goverment_departmet = 1
        plants_per_district = BlockPlantation.objects.filter(goverment_departmet=department,block_code=blockid).filter(
        number_of_plants__regex=r'^\d+$'  # Only include numeric values
        ).values('gp_code__GP_FINAL_N').annotate(
            total_plants=Sum(Cast('number_of_plants', IntegerField()))
        )
        # # # Example of accessing the results
        # for item in plants_per_district:
        #     print(f"District: {item['dict_code__DISTRICT_N']}, Total Plants: {item['total_plants']}")

        # Query to count repeated rows by dict_code where gov_department_id = 1
        repeated_rows_per_district = plantation_bygov.objects.filter(
            gov_department_id=department,block_code=blockid
        ).values('gp_code__GP_FINAL_N').annotate(
            count=Count('id')
        ).order_by('-count')
        # # Example of accessing the results
        # for item in repeated_rows_per_district:
        #     viewcount+=item['count']
        #     print(f"District: {item['dict_code__DISTRICT_N']}, Count: {item['count']}")

        # Convert to lists of dictionaries for JSON serialization
        block_plantation_list = list(plants_per_district)
        indivisual_plantation_list = list(repeated_rows_per_district)

        # print(block_plantation_list,indivisual_plantation_list)

        # Serialize the data to JSON
        block_plantation_data = json.dumps(block_plantation_list)
        indivisual_plantation_data = json.dumps(indivisual_plantation_list)
        department_name = json.dumps(department_name)
        blockname = json.dumps(blockname)

        context = {
            'block_plantation_data': block_plantation_data,
            'indivisual_plantation_data': indivisual_plantation_data,
            'department_name': department_name,
            'blockname': blockname,
        }
        # Process the department data as needed
        # For example, you could render a template or return a response
        return render(request, 'departmentdata/department_gp_excel.html', context)
    else:
        return HttpResponse("No department specified.")


def video_modal(request):
    return render(request, "video_modal.html")

def gallery_view(request):
    media_url = "/media/gallery/"  # Change this if your media URL is different
    gallery_dir = os.path.join(settings.MEDIA_ROOT, "gallery")
    images = []
    if os.path.exists(gallery_dir):
        images = [f"{media_url}{img}" for img in os.listdir(gallery_dir) if img.lower().endswith((".jpg", ".jpeg", ".png", ".gif"))]
    return render(request, "gallery.html", {"images": images})





