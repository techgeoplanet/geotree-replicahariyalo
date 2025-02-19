from rest_framework import viewsets
from .models import District, Block, GramPanchayat, Plant_List, NurseryDetails, ListOfPlantsInNursery
from .serializers import (
    DistrictSerializer,
    BlockSerializer,
    GramPanchayatSerializer,
    PlantListSerializer,
    NurseryDetailsSerializer,
    ListOfPlantsInNurserySerializer,
)
from account.renderers import UserRenderer
from api.permissions import IsAdminOrReadOnly ,IsPatnerOrReadOnly , IsPartnerWriteOrAuthenticatedRead, IsAdminWriteOrAuthenticatedRead
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed
from django.shortcuts import render, redirect ,get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required, permission_required



class DistrictViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminWriteOrAuthenticatedRead]
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def create(self, request, *args, **kwargs):
        # If the request data is a list, handle bulk creation
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class BlockViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminWriteOrAuthenticatedRead]
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

    def get_queryset(self):
        queryset = Block.objects.all()
        district_id = self.request.query_params.get('district')  # Get the 'district' parameter from the request
        if district_id:
            queryset = queryset.filter(District_id=district_id)  # Filter by district ID
        return queryset

    def create(self, request, *args, **kwargs):
        # If the request data is a list, handle bulk creation
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class GramPanchayatViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminWriteOrAuthenticatedRead]
    queryset = GramPanchayat.objects.all()
    serializer_class = GramPanchayatSerializer

    def get_queryset(self):
        queryset = GramPanchayat.objects.all()
        block_id = self.request.query_params.get('block')  # Get the 'block' parameter from the request
        if block_id:
            queryset = queryset.filter(block_id=block_id)  # Filter by block ID
        return queryset

    def create(self, request, *args, **kwargs):
        # If the request data is a list, handle bulk creation
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class PlantListViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAdminWriteOrAuthenticatedRead]
    queryset = Plant_List.objects.all()
    serializer_class = PlantListSerializer

    def create(self, request, *args, **kwargs):
        # If the request data is a list, handle bulk creation
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class NurseryDetailsViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPartnerWriteOrAuthenticatedRead]
    queryset = NurseryDetails.objects.all()
    serializer_class = NurseryDetailsSerializer

    def get_queryset(self):
        """
        Return all nurseries submitted by the currently authenticated user.
        """
        queryset = super().get_queryset()

        # Check if the user is authenticated
        if self.request.user.is_authenticated:
            queryset = queryset.filter(submitted_by=self.request.user)

        return queryset


    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')


class ListOfPlantsInNurseryViewSet(viewsets.ModelViewSet):
    renderer_classes = [UserRenderer]
    permission_classes = [IsPartnerWriteOrAuthenticatedRead]
    queryset = ListOfPlantsInNursery.objects.all()
    serializer_class = ListOfPlantsInNurserySerializer

    def create(self, request, *args, **kwargs):
        # If the request data is a list, handle bulk creation
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)
        

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PUT')

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed('PATCH')

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed('DELETE')

from django.core.cache import cache
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


class nurserydashview:
    @staticmethod
    def view(request):
        if not request.user.is_authenticated:
            return redirect('loginadm')

        # Fetch rows per page, defaulting to 10, and limit to 100
        rows_per_page = min(int(request.GET.get('rows', 10)), 100)
        page_number = request.GET.get('page', 1)

        # Retrieve filter inputs
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        grampanch_in = request.GET.get('grampanch_in')
        grampanch_t = request.GET.get('grampanch_t')
        block_in = request.GET.get('block_in')
        block_t = request.GET.get('block_t')
        district_in = request.GET.get('district_in')
        district_t = request.GET.get('district_t')

        # Initialize base queryset
        queryset = NurseryDetails.objects.order_by('-created_at')

        # Build filter conditions using Q objects
        filters = Q()
        if date_from and date_to:
            try:
                date_from_parsed = timezone.datetime.strptime(date_from, "%Y-%m-%d").date()
                date_to_parsed = timezone.datetime.strptime(date_to, "%Y-%m-%d").date()
                filters &= Q(created_at__date__range=(date_from_parsed, date_to_parsed))
            except ValueError:
                messages.error(request, "Invalid date format. Please use YYYY-MM-DD.")

        if grampanch_in:
            filters &= Q(gram_panchayat_id=grampanch_in)
        elif block_in:
            filters &= Q(gram_panchayat__block__block_id=block_in)
        elif district_in:
            filters &= Q(gram_panchayat__block__District__District_id=district_in)

        

        # Use caching for counts
        total_count = cache.get_or_set('total_count', queryset.count, timeout=300)
        today = timezone.now().date()
        today_count = cache.get_or_set(f'today_count_{today}', lambda: queryset.filter(created_at__date=today).count(), timeout=300)

        # Apply filters to queryset
        queryset = queryset.filter(filters)

        # print(total_count,today_count,"-----")

        # Pagination
        paginator = Paginator(queryset, rows_per_page)
        try:
            nursery_info = paginator.page(page_number)
        except (PageNotAnInteger, EmptyPage):
            nursery_info = paginator.page(1)

        # Handle selected rows
        selected_rows = request.POST.getlist('selected_rows', []) if request.method == 'POST' else []

        context = {
            'nursery_info': nursery_info,
            'rows_per_page': rows_per_page,
            'user': request.user,
            'selected_rows': selected_rows,
            'total_count': total_count,
            'today_count': today_count,
            'date_from': date_from,
            'date_to': date_to,
            'grampanch_in': grampanch_in,
            'grampanch_t': grampanch_t,
            'block_in': block_in,
            'block_t': block_t,
            'district_in': district_in,
            'district_t': district_t
        }

        return render(request, 'nurcery.html', context)

from django.http import JsonResponse ,HttpResponse
@login_required
@csrf_protect
def districtListView(request):
    try:
        districts = District.objects.all().values('District_id', 'District_name')
        district_list = list(districts)
        return JsonResponse({
            "success": True,
            "districts": district_list
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

@login_required
@csrf_protect
def blockListView(request):
    district_id = request.GET.get('district_id')
    if district_id:
        try:
            blocks = Block.objects.filter(District=district_id).values('block_id', 'block_name')
            return JsonResponse({
                "success": True,
                "blocks": list(blocks)
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

@login_required
@csrf_protect
def gpListView(request):
    block_id = request.GET.get('block_id')
    if block_id:
        try:
            gps = GramPanchayat.objects.filter(block=block_id).values('gp_id', 'gp_name')
            return JsonResponse({
                "success": True,
                "gps": list(gps)
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "error": str(e)
            }, status=500)

# this for download all btn 
import csv
from io import BytesIO
import logging
import pandas as pd


# Set up logging
logger = logging.getLogger(__name__)

@login_required
@csrf_protect
def downloadNurceryDataFull(request):
    try:
        # Fetch districts data from database
        nurcery_queryset = NurseryDetails.objects.all().values('nursery_id','nursery_name','depart_id__department_name','ownership', 'image_nursery','total_quantity_of_plants','total_type_of_plants','asfs_no','khasra_no','location_lat','location_long','location_filling','gram_panchayat__District__District_name','gram_panchayat__block__block_name','gram_panchayat__gp_name','submitted_by','status','created_at','updated_at','submitted_date')

        # Paginate the districts if necessary
        page_number = request.GET.get('page', 1)
        paginator = Paginator(nurcery_queryset, 1000)  # 1000 records per page
        page = paginator.get_page(page_number)

        # Create the CSV content in memory using Pandas
        csv_file = generate_csv(page)

        # Return the CSV as a downloadable response without compression
        response = create_csv_response(csv_file, page_number)
        return response

    except Exception as e:
        # Log the exception to the server logs
        logger.error(f"Error generating CSV: {e}", exc_info=True)
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=500)

def generate_csv(page):
    """
    Generates CSV content from a page of district data using Pandas.
    """
    # Convert queryset to DataFrame
    df = pd.DataFrame(page.object_list)  # page.object_list contains the paginated results

    # Create a BytesIO object to hold the CSV data in memory
    csv_file = BytesIO()
    
    # Write the DataFrame to the BytesIO object as CSV
    df.to_csv(csv_file, index=False, header=True)  # Don't include the index in the CSV
    
    # Seek to the start of the file
    csv_file.seek(0)
    
    return csv_file

def create_csv_response(csv_file, page_number):
    """
    Creates an HTTP response with the CSV file for download (without gzip compression).
    """
    # Ensure the correct content type for CSV
    response = HttpResponse(csv_file.read(), content_type='text/csv')
    
    # Set the content-disposition header to force download and name the file
    response['Content-Disposition'] = f'attachment; filename=districts_Maxrow_100_page_{page_number}.csv'
    
    # Log response headers to ensure everything is correct
    logger.info(f"Response headers: {response.items()}")
    
    return response