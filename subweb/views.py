from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from account.models import TempUser, User
from django.http import JsonResponse
import time
from .forms import PlantationByPvtForm, PlantationByGovForm, PlantationByNgoForm ,TempStorageCertificateInfoForm
from django.views import View
from django.utils.decorators import method_decorator
from api.models import *
from django.utils.crypto import get_random_string
import requests
from api.middleware import RequestLimitMiddleware
from django.conf import settings


def generate_otp(user):
    otp = get_random_string(length=4, allowed_chars='0123456789')
    otp_obj = OTP_model.objects.create(user_phone=user, otp=otp)
    return otp

def send_otp(phone):
    phone = phone  # Assuming user is logged in
    otp = generate_otp(phone)
    # url='https://loadcrm.com/SmsApi/'

    # current opratable 
    # url = f"https://loadcrm.com/SmsApi/api/OwnApi/SendSms?key=SEAMWTOQ2ZWX47KEBPDZOP===&UserName=Geoplanet&SenderID=GEOPLT&MessageText=Your OTP Is {otp} - GEO Planet&EntityId=1101614800000080255&TemplateId=1107171946625040560&Unicode=false&MobileNo={phone}"
   
   
    # url = f"https://loadcrm.com/SmsApi/api/OwnApi/SendSms?key=MFCWS3VBO0VNOSTHI8WAF1===&UserName=ZubairSMS&SenderID=LOADIT&MessageText={otp} OTP for GR enterprises&EntityId=1201159135635312494&TemplateId=1207162046687693066&Unicode=false&MobileNo={phone}"

    # url = f"{settings.SMS_OTP_API_URL}?key={settings.SMS_OTP_API_KEY}===&UserName=Geoplanet&SenderID={settings.SMS_OTP_SENDER_ID}&MessageText=Your OTP Is {otp} - GEO Planet&EntityId={settings.SMS_OTP_ENTITY_ID}&TemplateId={settings.SMS_OTP_TEMPLATEID_ID}&Unicode=false&MobileNo={phone}"

    # response = requests.get(url)
    # if response.status_code == 200:
    #     return True
    # else:
    #     return False

    return otp


# this sectoin is for login 
@csrf_protect
def tempuser_login(request):
    
    context = {
        'is_sent': False
    }
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        otp = request.POST.get('otp')
        
        if otp:
            try:
                user = TempUser.objects.get(phone=phone)
                otp_obj = OTP_model.objects.filter(user_phone=phone).latest('created_at')
                
                if otp_obj.otp == otp and otp_obj.expiration_time > timezone.now():
                    # otp_obj.delete()
                    auth_login(request, user, backend='account.authentication.TempUserBackend')
                    return redirect(reverse('hi-home'))  # Redirect to add_tempdata view
                else:
                    context = {
                        'is_sent': True,
                        'phonenumber':phone,
                        'message':'Wrong OTP',
                        'opt_captcha':otp_obj.otp,
                        }
                     # return HttpResponse('oyp send')
                    return render(request, 'tempuser_login.html', context)
                
            except TempUser.DoesNotExist:
                return HttpResponse('User does not exist ')
        else:
            user, created = TempUser.objects.get_or_create(phone=phone)
            sent = send_otp(phone)
            if sent:
                otp_expiration_time = timezone.now() + timedelta(minutes=10)
                context = {
                    'is_sent': True,
                    'phonenumber':phone,
                    'message':'Captcha Generate successfully',
                    'otp_expiration_time':otp_expiration_time,
                    'opt_captcha':sent, 
                    }
                # return HttpResponse('oyp send')
                return render(request, 'tempuser_login.html', context)
            else:
                context = {
                    'is_sent': False,
                    'phonenumber':phone,
                    'message':'OTP Not Sending',
                    'otp_expiration_time':time.time()
                    }
                # return HttpResponse('oyp send')
                return render(request, 'tempuser_login.html', context)
            
    return render(request, 'tempuser_login.html', context)



# this is opsational fiels 
@csrf_protect
def customuser_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user, backend='account.authentication.CustomUserBackend')
            return redirect('add-tempdata')  # Redirect to a logged-in homepage or dashboard
        else:
            return HttpResponse('Invalid login credentials.')
    return render(request, 'customuser_login.html')


@csrf_protect
def customuser_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        department = request.POST.get('department')
        tc = request.POST.get('tc')
        password = request.POST.get('password')
        user = User.objects.create_user(email=email, name=name, department=department, tc=tc, password=password)
        auth_login(request, user, backend='account.authentication.CustomUserBackend')
        return redirect('add-tempdata')  # Redirect to a logged-in homepage or dashboard
    return render(request, 'customuser_register.html')


# this section for test perpose 
#https://www.youtube.com/watch?v=vLOe61zD620
@login_required
@csrf_protect
def add_tempdata(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:
            # Process the data as needed
            response = JsonResponse({"success": True, "data": data})
            return response  # Return JSON response for successful POST request
        
        else:  # If 'data' parameter is missing in POST request
            error_message = "Missing 'data' parameter"
            return JsonResponse({"success": False, "error": error_message}, status=400)
    
    # If it's not a POST request, render the template with additional context
    context = {
        'is_sent': True
    }
    return render(request, 'add_tempdata.html', context)


# for logout view 
@login_required
def logout_view(request):
    if request.user.is_authenticated:
        if request.user.id in RequestLimitMiddleware.authenticated_requests:
            del RequestLimitMiddleware.authenticated_requests[request.user.id]

    auth_logout(request)
    return redirect('tempuser_login')


# open home page 
@login_required
@csrf_protect
def home_page(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:  # Check if it's an Ajax request
            # print(data)
            response = JsonResponse({"data": data})
            return response  # Return JSON response for Ajax request
        
        else:  # If 'data' parameter is missing in POST request
            error_message = "Missing 'data' parameter"
            return JsonResponse({"error": error_message}, status=400)
    
    # If it's not a POST request, render the template with additional context
    context = {
        'is_sent': True
    }
    return render(request, 'home.html', context)

# open home page 
@login_required
@csrf_protect
def hi_home_page(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        if data:  # Check if it's an Ajax request
            # print(data)
            response = JsonResponse({"data": data})
            return response  # Return JSON response for Ajax request
        
        else:  # If 'data' parameter is missing in POST request
            error_message = "Missing 'data' parameter"
            return JsonResponse({"error": error_message}, status=400)
    
    # If it's not a POST request, render the template with additional context
    context = {
        'is_sent': True
    }
    return render(request, 'hi/home.html', context)


# for add new plantation 
@login_required
@csrf_protect
def addplant_normaluser_page(request):
    # if request.method == 'POST':
    #     form = PlantForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return JsonResponse({'message': 'Plant added successfully!'}, status=200)
    #     else:
    #         return JsonResponse({'errors': form.errors}, status=400)
    # else:
    #     form = PlantForm()

    departments = gov_department.objects.order_by('department_name')
        
    return render(request, 'addplant.html',{'departments': departments})


# for add new plantation 
@login_required
@csrf_protect
def hi_addplant_normaluser_page(request):
    # if request.method == 'POST':
    #     form = PlantForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return JsonResponse({'message': 'Plant added successfully!'}, status=200)
    #     else:
    #         return JsonResponse({'errors': form.errors}, status=400)
    # else:
    #     form = PlantForm()

    departments = gov_department.objects.order_by('department_name')    
    return render(request, 'hi/addplant.html',{'departments': departments})

from portaldash.signal import update_short_table

class CreatePlantationPvtView(View):
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # print("Incoming POST data:", request.POST)
        form = PlantationByPvtForm(request.POST, request.FILES)
        gp_code_id = self.request.POST.get('gp_code')
        # print(form)
        if form.is_valid():
            plant = form.save(commit=False)
            plant.submitted_by = request.user  # Set the submitted_by field to the current user
            plant.save()
            # Update the short table if gp_code_id is present
            if gp_code_id:
                update_short_table(
                    GP_FINAL_C=gp_code_id,
                    update_field='Total_Tag_Tree_Non_Verify_C',
                    increment_value=1
                )

            return JsonResponse({'success': True, 'plantation_id_bypvt': plant.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class CreatePlantationGovView(View):
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PlantationByGovForm(request.POST, request.FILES)
        gp_code_id = self.request.POST.get('gp_code')
        if form.is_valid():
            plant = form.save(commit=False)
            plant.submitted_by = request.user  # Set the submitted_by field to the current user
            plant.save()
            if gp_code_id:
                update_short_table(
                    GP_FINAL_C=gp_code_id,
                    update_field='Total_Tag_Tree_Non_Verify_C',
                    increment_value=1
                )

            # print('plantation_id_bygov',plant.id)
            return JsonResponse({'success': True, 'plantation_id_bygov': plant.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class CreatePlantationNgoView(View):
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = PlantationByNgoForm(request.POST, request.FILES)
        gp_code_id = self.request.POST.get('gp_code')
        if form.is_valid():
            plant = form.save(commit=False)
            plant.submitted_by = request.user  # Set the submitted_by field to the current user
            plant.save()
            if gp_code_id:
                update_short_table(
                    GP_FINAL_C=gp_code_id,
                    update_field='Total_Tag_Tree_Non_Verify_C',
                    increment_value=1
                )
            return JsonResponse({'success': True, 'plantation_id_byngo': plant.id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

class CreateTempStorageCertificateInfoView(View):
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        # print("Incoming POST data:", request.POST)
        form = TempStorageCertificateInfoForm(request.POST, request.FILES)
        if form.is_valid():
            cert_info = form.save(commit=False)
            cert_info.user_id = request.user  # Set the user_id field to the current user
            cert_info.save()
            return JsonResponse({'success': True, 'certificate_id': cert_info.certificate_id})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})


import json
@login_required
@csrf_protect
def rewards_viewset(request):
    user_id = request.user
        
    # Filter records from each plantation table based on user_id and status=True
    plantations_pvt = plantation_bypvt.objects.filter(submitted_by=user_id, status=True).values('plantation_name', 'created_at')
    plantations_gov = plantation_bygov.objects.filter(submitted_by=user_id, status=True).values('plantation_name', 'created_at')
    plantations_ngo = plantation_byngo.objects.filter(submitted_by=user_id, status=True).values('plantation_name', 'created_at')

    # Combine results into a single dictionary
    tree_records = {
        'private': list(plantations_pvt),
        'government': list(plantations_gov),
        'ngo': list(plantations_ngo)
    }

    return render(request, 'rewards.html', {'tree_records': tree_records})

@login_required
@csrf_protect
def hi_rewards_viewset(request):
    user_id = request.user
        
    # Filter records from each plantation table based on user_id and status=True
    plantations_pvt = plantation_bypvt.objects.filter(submitted_by=user_id, status=True).values('plantation_name', 'created_at')
    plantations_gov = plantation_bygov.objects.filter(submitted_by=user_id, status=True).values('plantation_name', 'created_at')
    plantations_ngo = plantation_byngo.objects.filter(submitted_by=user_id, status=True).values('plantation_name', 'created_at')

    # Combine results into a single dictionary
    tree_records = {
        'private': list(plantations_pvt),
        'government': list(plantations_gov),
        'ngo': list(plantations_ngo)
    }

    return render(request, 'hi/rewards.html', {'tree_records': tree_records})

# for tips page 
def tips_viewset(request):
    return render(request, 'plantationtips.html')

# for tips page 
def hi_tips_viewset(request):
    return render(request, 'hi/plantationtips.html')


# for more info page 
def moreinformation_viewset(request):
    return render(request, 'more_info/more_info.html')

# for more info page 
def hi_moreinformation_viewset(request):
    return render(request, 'hi/more_info/more_info.html')


# for certificate system 
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from django.conf import settings
import os


def generate_certificate_number(user):
    # Implement a logic to generate a unique certificate number
    return f"CERT-{user}-{int(time.time())}"


@login_required
@csrf_protect
def save_certificate_info(request):
    return render(request, 'certificate/certificat_submit.html')
    

@login_required
@csrf_protect
def get_certificate_template(request):
    template_path = os.path.join(settings.BASE_DIR, 'private', 'certificates', 'c1.webp')
    try:
        with open(template_path, 'rb') as template_file:
            response = HttpResponse(template_file.read(), content_type='image/webp')
            response['Content-Disposition'] = 'inline; filename="c1.webp"'
            return response
    except FileNotFoundError:
        raise Http404("Template not found")


@login_required
def certificate_view(request):
    user = request.user
    certificates = TempStorageCertificateInfo.objects.filter(user_id=user).order_by('created_at')
    # print(certificates)
    return render(request, 'certificate/certificat.html', {'data': certificates})


@login_required
def hi_certificate_view(request):
    user = request.user
    certificates = TempStorageCertificateInfo.objects.filter(user_id=user).order_by('created_at')
    return render(request, 'hi/certificate/certificat.html', {'data': certificates})


@login_required
def my_pvt_history_viewset(request):
    user = request.user
    filtered_data = plantation_bypvt.objects.filter(submitted_by=user).order_by('-updated_at')
    return render(request, 'history/my_pvt_plantation_history.html', {'data': filtered_data})

@login_required
def my_ngo_history_viewset(request):
    user = request.user
    filtered_data = plantation_byngo.objects.filter(submitted_by=user).order_by('-updated_at')
    return render(request, 'history/my_ngo_plantation_history.html', {'data': filtered_data})

@login_required
def my_gov_history_viewset(request):
    user = request.user
    filtered_data = plantation_bygov.objects.filter(submitted_by=user).order_by('-updated_at')
    return render(request, 'history/my_gov_plantation_history.html', {'data': filtered_data})

# for hindi 
@login_required
def hi_my_pvt_history_viewset(request):
    user = request.user
    filtered_data = plantation_bypvt.objects.filter(submitted_by=user).order_by('-updated_at')
    return render(request, 'hi/history/my_pvt_plantation_history.html', {'data': filtered_data})

@login_required
def hi_my_ngo_history_viewset(request):
    user = request.user
    filtered_data = plantation_byngo.objects.filter(submitted_by=user).order_by('-updated_at')
    return render(request, 'hi/history/my_ngo_plantation_history.html', {'data': filtered_data})

@login_required
def hi_my_gov_history_viewset(request):
    user = request.user
    filtered_data = plantation_bygov.objects.filter(submitted_by=user).order_by('-updated_at')
    return render(request, 'hi/history/my_gov_plantation_history.html', {'data': filtered_data})


def checkcam(request):
    return render(request,'camera_model.html')
