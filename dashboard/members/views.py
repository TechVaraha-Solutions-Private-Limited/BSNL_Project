from django.shortcuts import render,redirect, HttpResponse, get_object_or_404
from django.http import JsonResponse
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee,TeamLead,Executive,SeniorTeamLead
from .models import Bookings,PaymentDetails,Ugdg,Images,Leadowner,Site_visit,Btmt,G_image,Request_call,LandDetails
from dashboard.projects.models import Project,PlotSize,LandDetails
from django.forms.models import model_to_dict
from django.contrib import messages
from django.db.models import Q,Sum
from django.contrib.auth.hashers import make_password
from dashboard.members.models import Update_blocked
from datetime import date,datetime
from .models import pdc_update
from django.http import HttpResponseServerError

from .models import Bookings 

from .models import LandDetails
from django.db.models import Count
from collections import defaultdict

#this mail
# from django.core.mail import send_mail
# from django.http import HttpResponse


# Create your views here.
def banner_images(request):
    if request.method =='POST':
        Images(
            images=request.FILES.get('profile', ''),
            place = "Banner"
        ).save()        
    return render(request,'image/banner.html')

def gallery_images(request):
    if request.method == 'POST':
        G_image(
            gallery_image=request.FILES.get('profile', ''),
            g_place= "gallery"
        ).save()
    return render(request,'image/gallery.html')




def home(request):
    project_details = []

   
    unique_projects = LandDetails.objects.values('project__projectname', 'plotsize__plotsize').annotate(land_count=Count('bookings'))
    if not unique_projects:
    
        context = {
            'message': "No projects found."
        }
        return render(request, 'common/index.html', context)
    
    for project in unique_projects:
        project_name = project['project__projectname']
        plot_size = project['plotsize__plotsize']
        land_count = project['land_count']
        
        split = plot_size.split("X")
        length = int(split[0])
        width   = int(split[1])

        tot_sq  = length*width*land_count

        project_details.append({
            'name': project_name,
            'size': plot_size,
            'land_count': land_count,
            'tot_sq': tot_sq
            
        })
        
    context = {
        'project_details': project_details
    }
    

    return render(request, 'common/index.html', context)
def addcustomer(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        mobile_no = request.POST.get('mobile_no')
        # send_mail(
        #     'good morning', 
        #     'hi come to join', 
        #     'mpsa1409@gmail.com',  # Sender's email address
        #     [email],  # List of recipients
        #     fail_silently=False,
        # )
        if not first_name :
            messages.error(request,'Enter the Name')
        else:
            user=User()
            user.first_name=first_name
            user.last_name=request.POST.get('last_name')
            user.mobile_no = mobile_no
            user.password = make_password(request.POST.get('password','').strip())
            user.role = "Customer"
            user.save()
            details = UserDetail()
            details.user = user
            details.dob = request.POST.get('dob')
            details.age = request.POST.get('age')
            details.email = request.POST.get('email')
            details.alternate_no = request.POST.get('alternate_no')
            details.aadhhaarno = request.POST.get('aadhhaarno')
            details.aadhar_proof = request.POST.get('aadhar_proof')
            details.panno = request.POST.get('panno')
            details.pan_proof = request.POST.get('pan_proof')
            details.profile = request.POST.get('profile')
            details.address = request.POST.get('address')
            details.city = request.POST.get('city')
            details.state = request.POST.get('state')
            details.save()

            nominee = UserNominee()
            nominee.user = user
            nominee.nominee_name = request.POST.get('nominee_name')
            nominee.nominee_age = request.POST.get('nominee_age')
            nominee.address = request.POST.get('address1')
            nominee.city = request.POST.get('city1')
            nominee.state = request.POST.get('state1')
            nominee.nominee_relationship = request.POST.get('nominee_relationship')
            nominee.save()

            check_input_no = request.POST.get('check_input_no')
            for val in range(int(check_input_no)): 
                member_name_key = f'member_name{val+1}'        
                member_age_key = f'member_age{val+1}'
                member_relation_key = f'member_relation{val+1}'

                family = UserFamilyDetails()
                family.user = user
                family.member_name = request.POST.get(member_name_key)
                family.member_age = request.POST.get(member_age_key)
                family.member_relation = request.POST.get(member_relation_key)
                family.save()
    return render(request,'new_bookings/addcustomer.html')

def site_visit_custmer(request,id):
    try:
        site_visit = Site_visit.objects.filter(id=id)
        projects = Project.objects.all()
        landdetail = LandDetails.objects.all()
        
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            mobile_no = request.POST.get('mobile_no')
            seniority_id = request.POST.get('seniority_id')
            
            user = User()
            user.first_name = first_name
            user.last_name = request.POST.get('last_name')
            user.mobile_no = mobile_no
            
            user.password = make_password(request.POST.get('password','').strip())
            user.role = "Customer"
            user.save()
            
            details = UserDetail()
            details.user = user
            details.dob = request.POST.get('dob')
            details.age = request.POST.get('age')
            details.email = request.POST.get('email')
            details.alternate_no = request.POST.get('alternate_no')
            details.aadhhaarno = request.POST.get('aadhhaarno')
            details.aadhar_proof = request.POST.get('aadhar_proof')
            details.panno = request.POST.get('panno')
            details.pan_proof = request.POST.get('pan_proof')
            details.profile = request.POST.get('profile')
            details.address = request.POST.get('address')
            details.city = request.POST.get('city')
            details.state = request.POST.get('state')
            details.save()
            nominee = UserNominee()
            nominee.user = user
            nominee.nominee_name = request.POST.get('nominee_name')
            nominee.nominee_age = request.POST.get('nominee_age')
            nominee.address = request.POST.get('address1')
            nominee.city = request.POST.get('city1')
            nominee.state = request.POST.get('state1')
            nominee.nominee_relationship = request.POST.get('nominee_relationship')
            nominee.save()
            check_input_no = request.POST.get('check_input_no')
            for val in range(int(check_input_no)): 
                member_name_key = f'member_name{val+1}'        
                member_age_key = f'member_age{val+1}'
                member_relation_key = f'member_relation{val+1}'

                family = UserFamilyDetails()
                family.user = user
                family.member_name = request.POST.get(member_name_key)
                family.member_age = request.POST.get(member_age_key)
                family.member_relation = request.POST.get(member_relation_key)
                family.save()
            
            get_last_number = PaymentDetails.objects.all().order_by('-id')[:1]
            if get_last_number: 
                auto_genrate = "AM-" + str(get_last_number[0].id + 1).zfill(5)
            else:
                auto_genrate = "AM-00001" 
            #end
            project_id = request.POST.get('projectname')
            dimension_id = request.POST.get('selectDimension')
            land_detail = LandDetails.objects.get(project_id=project_id,plotsize_id=dimension_id)
            book = Bookings()
            book.user = user
            book.membership_id = request.POST.get('seniority_id')
            book.seniority_id = request.POST.get('seniority_id')
            book.land_details = land_detail
            book.total_site_value = request.POST.get('total_site_value')
            book.downpayment = request.POST.get('downpayment')
            book.site_refer = request.POST.get('site_refer')
            book.sitevist_id = id
            book.am_no = auto_genrate
            book.save()
            #vicky
            split_amount = int(book.total_site_value) / 4
            paid_amount =  request.POST.get('amount','').strip()
            payment_amount = int(paid_amount) -2260

            if paid_amount:

                membership_fee = PaymentDetails()
                membership_fee.booking=book

                membership_fee.payment_mode = request.POST.get('payment_mode')
                membership_fee.bank = request.POST.get('bank')
                membership_fee.branch = request.POST.get('branch')
                membership_fee.cheque_no = request.POST.get('cheque_no')
                membership_fee.transaction = request.POST.get('transaction_id')
                membership_fee.ddno=request.POST.get('dd_no')
                membership_fee.user = user
                membership_fee.payment_data = request.POST.get('payment_data')
                
                membership_fee.amount = 2260
                membership_fee.paymentname = "Membership"
                get_number = PaymentDetails.objects.all().order_by('-id')[:1]
                if get_number:
                    get_number = "B-" + str(get_number[0].id + 1).zfill(5)
                else:
                    get_number = "B-00001" 
                membership_fee.receipt_no = get_number
                membership_fee.save()

                for i in range(4):
                    if i == 0:
                        paymentname = 'DownPayment'
                        status =1 
                    elif i ==1:
                        status =3
                        paymentname = 'FirstInstallment'
                    elif i == 2:
                        status =5
                        paymentname = 'SecondInstallment'
                    else:
                        status =7
                        paymentname = 'ThridInstallment'
                    get_number = PaymentDetails.objects.all().order_by('-id')[:1]
                    if get_number:
                        get_number = "B-" + str(get_number[0].id + 1).zfill(5)
                    else:
                        get_number = "B-00001" 
                    if split_amount  < payment_amount:
                        payments = PaymentDetails()
                        payments.booking=book

                        payments.payment_mode = request.POST.get('payment_mode')
                        payments.bank = request.POST.get('bank')
                        payments.branch = request.POST.get('branch')
                        payments.cheque_no = request.POST.get('cheque_no')
                        payments.transaction = request.POST.get('transaction_id')
                        payments.ddno=request.POST.get('dd_no')
                        payments.user = user
                        payments.payment_data = request.POST.get('payment_data')
                        payments.paymentname =paymentname
                        payments.amount = split_amount
                        payments.receipt_no = get_number
                        payments.total_paid_amount =int(book.total_paid_amount )+ int(paid_amount)
                        payments.save()
                        payment_amount = payment_amount - split_amount 
                    elif payment_amount > 0:
                    
                        payments = PaymentDetails()
                        payments.booking=book

                        payments.payment_mode = request.POST.get('payment_mode')
                        payments.bank = request.POST.get('bank')
                        payments.branch = request.POST.get('branch')
                        payments.cheque_no = request.POST.get('cheque_no')
                        payments.transaction = request.POST.get('transaction_id')
                        payments.ddno=request.POST.get('dd_no')
                        payments.user = user
                        payments.payment_data = request.POST.get('payment_data')
                        payments.paymentname =paymentname
                        payments.amount = payment_amount
                        payments.receipt_no = get_number
                        payments.save()
                        book.payments_status = status
                        book.total_paid_amount =int(book.total_paid_amount )+ int(paid_amount)
                        book.save()
                        break
        messages.success(request,'Successfully Saved')
        # Vicky    
    
        return render(request, 'new_bookings/add_new_bookings.html',{'landdetail':landdetail,'projects':projects,'site_visit':site_visit})
    except Exception as e:
        messages.error(request, f'Error occurred: {e}')
        return HttpResponseServerError('Internal Server Error')
def add_new_bookings(request):
    projects = Project.objects.all()
    landdetail = LandDetails.objects.all()
    exectiv = User.objects.filter(role='Executive')
    errors = []
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        seniority_id = request.POST.get('seniority_id')
    
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, 'Email already exists. Please use a different email.')
        #     return render(request, 'new_bookings/add_new_bookings.html', {'landdetail': landdetail, 'projects': projects})

        # if User.objects.filter(mobile_no=mobile_no).exists():
        #     messages.error(request, 'Mobile number already exists. Please use a different mobile number.')
        #     return render(request, 'new_bookings/add_new_bookings.html', {'landdetail': landdetail, 'projects': projects})
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'new_bookings/add_new_bookings.html', {'landdetail': landdetail, 'projects': projects})

        try:
            user = User()
            user.first_name = first_name
            user.last_name = request.POST.get('last_name')
            user.mobile_no = mobile_no
            user.password = make_password(request.POST.get('password', '').strip())
            user.role = "Customer"
            seniority_id=seniority_id
            user.save()

            details = UserDetail()
            details.user = user
            details.dob = request.POST.get('dob')
            details.age = request.POST.get('age')
            details.email = request.POST.get('email')
            details.alternate_no = request.POST.get('alternate_no')
            details.aadhhaarno = request.POST.get('aadharno')
            details.aadhar_proof = request.POST.get('aadhar_proof')
            details.panno = request.POST.get('panno')
            details.pan_proof = request.POST.get('pan_proof')
            details.profile = request.POST.get('profile')
            details.address = request.POST.get('address')
            details.city = request.POST.get('city')
            details.state = request.POST.get('state')
            details.pincode = request.POST.get('pincode')
            details.save()

            nominee = UserNominee()
            nominee.user = user
            nominee.nominee_name = request.POST.get('nominee_name')
            nominee.nominee_age = request.POST.get('nominee_age')
            nominee.address = request.POST.get('address1')
            nominee.city = request.POST.get('city1')
            nominee.state = request.POST.get('state1')
            nominee.nominee_relationship = request.POST.get('nominee_relationship')
            nominee.save()

            check_input_no = request.POST.get('check_input_no')
            for val in range(int(check_input_no)):
                member_name_key = f'member_name{val + 1}'
                member_age_key = f'member_age{val + 1}'
                member_relation_key = f'member_relation{val + 1}'

                family = UserFamilyDetails()
                family.user = user
                family.member_name = request.POST.get(member_name_key)
                family.member_age = request.POST.get(member_age_key)
                family.member_relation = request.POST.get(member_relation_key)
                family.save()

            get_last_number = PaymentDetails.objects.all().order_by('-id')[:1]
            if get_last_number:
                auto_generate = "AM-" + str(get_last_number[0].id + 1).zfill(5)
            else:
                auto_generate = "AM-00001"

            project_id = request.POST.get('projectname')
            dimension_id = request.POST.get('selectDimension')
            land_details = LandDetails.objects.filter(project_id=project_id, plotsize_id=dimension_id).first()

            exective_id = request.POST.get('executive')
            if not exective_id:

                messages.error(request, 'Please select an executive.')
                return render(request, 'new_bookings/add_new_bookings.html', {'landdetail': landdetail, 'exectiv': exectiv, 'projects': projects})
            value = User.objects.get(id=exective_id)
            get_execute = Executive.objects.get(user_id=value.id)
            team_lead_user = get_execute.teamlead.user
        
            # teamlead = User.objects.get(id=teamlead_id)
            project_lead_id = get_execute.teamlead.sr_team.project_head.id
            project_lead = User.objects.get(id=project_lead_id)
        
            book = Bookings()
            book.user = user
            book.mobile_no = mobile_no
            book.membership_id = request.POST.get('member_id')
            book.seniority_id = request.POST.get('seniority_id')
            book.land_details = land_details
            book.total_site_value = request.POST.get('total_site_value')
            book.downpayment = request.POST.get('downpayment')
            book.site_refer = request.POST.get('site_refer')
            book.am_no = auto_generate
            book.executive = value
            book.teamlead = team_lead_user
            book.projhead = project_lead

            book.save()

            split_amount = int(book.total_site_value) / 4

            paid_amount =  request.POST.getlist('amount[]')
            payment_mode = request.POST.getlist('payment_mode[]')
            bank = request.POST.getlist('bank[]')
            branch = request.POST.getlist('branch[]')
            cheque_no = request.POST.getlist('cheque_no[]')
            transaction_id = request.POST.getlist('transaction_id[]')
            ddno=request.POST.getlist('dd_no[]')
            #dateofreceipt = request.POST.get('dateofreceipt')


            get_number = PaymentDetails.objects.all().order_by('-id')[:1]
            if get_number:
                get_number = "634" + str(get_number[0].id + 1)
            else:
                get_number = "63421"        
            #paid_amount = request.POST.get('amount', '').strip()
            for count in range(len(payment_mode)):
                if count == 0:
                    payment_amount = int(paid_amount[count]) - 2600
                else:
                    payment_amount = int(paid_amount[count])  # No subtraction after the first time

                if paid_amount[count]:
                    if count == 0:
                        membership_fee = PaymentDetails()
                        membership_fee.booking = book
                        membership_fee.payment_mode = payment_mode[count]
                        membership_fee.bank = bank[count]
                        membership_fee.branch = branch[count]
                        membership_fee.cheque_no = cheque_no[count]
                        membership_fee.transaction = transaction_id[count]
                        membership_fee.ddno = ddno[count]
                        membership_fee.user = user
                        membership_fee.dateofreceipt = date.today()
                        membership_fee.amount = 2600
                        membership_fee.paymentname = "Membership"
                        membership_fee.receipt_no = get_number
                        membership_fee.save()
                    for i in range(4):
                        print ("I",i,count)
                        if i == 0 and count == 0:
                            paymentname = 'DownPayment'
                            status = 1
                        elif i == 0 and count == 1:
                            status = 3
                            paymentname = 'FirstInstallment'
                        elif i == 0 and count == 2:
                            status = 5
                            paymentname = 'SecondInstallment'
                        else:
                            status = 7
                            paymentname = 'ThirdInstallment'
                        # get_number = PaymentDetails.objects.all().order_by('-id')[:1]
                        # if get_number:
                        #     get_number = "634" + str(get_number[0].id + 1)
                        # else:
                        #     get_number = "63421"
                        if split_amount <= payment_amount :
                            print("payment",payment_amount)
                            payments = PaymentDetails()
                            payments.booking = book
                            payments.payment_mode = payment_mode[count]
                            payments.bank = bank[count]
                            payments.branch = branch[count]
                            payments.cheque_no = cheque_no[count]
                            payments.transaction = transaction_id[count]
                            payments.ddno = ddno[count]
                            payments.user = user
                            #payments.payment_data = request.POST.get('payment_data')
                            payments.paymentname = paymentname
                            payments.amount = int(split_amount)
                            payments.receipt_no = get_number
                            payments.dateofreceipt = date.today()
                            payments.save()
                           
                            payment_amount = payment_amount - split_amount
                        elif payment_amount > 0 :
                            payments = PaymentDetails()
                            payments.booking = book
                            payments.payment_mode = payment_mode[count]
                            payments.bank = bank[count]
                            payments.branch = branch[count]
                            payments.cheque_no = cheque_no[count]
                            payments.transaction = transaction_id[count]
                            payments.ddno = ddno[count]
                            payments.user = user
                            #payments.payment_data = request.POST.get('payment_data')
                            payments.paymentname = paymentname
                            payments.amount = int(payment_amount) 
                            payments.receipt_no = get_number
                            payments.dateofreceipt = date.today()
                            payments.save()
                            
                            
                        break
            messages.success(request, 'Successfully Saved')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')    

    
    return render(request, 'new_bookings/add_new_bookings.html', {'landdetail': landdetail,'exectiv':exectiv,'projects': projects})
def get_dimension(request):
    if request.method == "POST":
        id = request.POST.get('id','').strip()
        dimensions = PlotSize.objects.filter(landdetails__project=id).values()
        project_details = Project.objects.get(id=id)
        return JsonResponse({"values":list(dimensions),'shortcut':project_details.shortcode})
    return JsonResponse({})

def get_project_value(request):
    if request.method == "POST":
        project_id = request.POST.get('project_id','').strip()
        plot_id = request.POST.get('plot_id','').strip()
        id = request.POST.get('project_id','').strip()
        dimensions = LandDetails.objects.filter(project_id=project_id,plotsize_id=plot_id).values()
        return JsonResponse({"values":list(dimensions)})
    return JsonResponse({})

def get_project_id(request):
    try:
        if request.method == "POST":
            plot_id = request.POST.get('plot_id','').strip()
            dimensions = LandDetails.objects.filter(project=plot_id).values()
            print(dimensions)
            return JsonResponse({"values": list(dimensions)})
        else:
            return JsonResponse({})
    except Exception as e:
        # Log the error or handle it appropriately
        print(f"Error occurred: {e}")
        return JsonResponse({"error": "An error occurred while processing the request"})

def booksum(request):
    view = User.objects.filter(role='Team_Lead')  
    
    project_details = []

    unique_projects = LandDetails.objects.values('project__projectname', 'plotsize__plotsize').annotate(land_count=Count('bookings'))
   
    for project in unique_projects:
        project_name = project['project__projectname']
        plot_size = project['plotsize__plotsize']
        land_count = project['land_count']
        
        split = plot_size.split("X")
        length = int(split[0])
        width   = int(split[1])

        tot_sq  = length*width*land_count
        sq_feet = length*width
        project_details.append({
            'name': project_name,
            'size': plot_size,
            'land_count': land_count,
            'tot_sq': tot_sq,
            'sq_feet':sq_feet
        })
        
    context = {
        'project_details': project_details,
        'view':view
        
    }
    



    return render(request,'home/booksum.html',context)

def bss(request):
   
    
    return render(request,'home/bss.html')

def print_receipt(request):
    return render('reports/print_recepit.html')

def generate(request):
    customers = {}
    total_site_value = 0
    payment_total = 0
    active_bookings = Bookings.objects.filter(user__is_active=1).order_by('-created_on').all()

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
               
                customers = Bookings.objects.get(seniority_id=seniority_id)

               
                payment = PaymentDetails.objects.filter(booking_id=customers.id).aggregate(Sum('amount'))
                payment_total = payment['amount__sum'] or 0  
                total_site_value = customers.total_site_value

                if not customers:
                    messages.error(request, 'Profile details updated.')
            except Bookings.DoesNotExist:
                messages.error(request, 'Invalid seniority ID. ')
                customers = {}       
        elif action == 'create_order':
            print('User ID:',user_id)
            seniority = request.POST.get('seniority')
            customers = Bookings.objects.get(seniority_id=seniority)
            payment = PaymentDetails.objects.filter(booking_id = customers.id).aggregate(Sum('amount'))                
            payment_total = payment['amount__sum'] or 0  
            total_site_value = customers.total_site_value
            book = Bookings.objects.get(user_id=user_id, seniority_id=seniority)
            payment = PaymentDetails.objects.filter(booking_id = book.id).aggregate(Sum('amount'))
            
            PaymentDetails()
            try:
                
                get_number = PaymentDetails.objects.all().order_by('-id')[:1]
                if get_number:
                    get_number = "634" + str(get_number[0].id + 1)
                else:
                    get_number = "63421"
                divide_amount = int(book.total_site_value) / 4
                split_amount = int(divide_amount)
                print('sp:',split_amount)
                paid_amount =  request.POST.getlist('amount[]')
                payment_mode = request.POST.getlist('payment_mode[]')
                bank = request.POST.getlist('bank[]')
                branch = request.POST.getlist('branch[]')
                cheque_no = request.POST.getlist('cheque_no[]')
                transaction_id = request.POST.getlist('transaction_id[]')
                ddno=request.POST.getlist('dd_no[]')
                dateofreceipt = request.POST.get('dateofreceipt')
                # payment_data = request.POST.get('payment_data')
                # paymenttype = request.POST.get('paymenttype')
                
                    
                
                #paid_amount =  request.POST.getlist('amount','').strip()
                print('pa:',paid_amount)
                
                difference = int(total_site_value) - int(payment_total)
                print('differ:',difference)
                
                # Need to resolve
                
                for count in range(len(payment_mode)): 
                    #payment_amount = int(paid_amount[count])-int(difference)
                    if paid_amount[count]:
                        if int(payment_total) < 2600: 
                            #payment_amount = int(paid_amount[count])-2600
                        
                        
                            membership_fee = PaymentDetails()
                            membership_fee.booking=book
                            membership_fee.payment_mode = payment_mode[count]
                            membership_fee.bank = bank[count]
                            membership_fee.branch = branch[count]
                            membership_fee.cheque_no = cheque_no[count]
                            membership_fee.transaction = transaction_id[count]
                            membership_fee.ddno=ddno[count]
                            membership_fee.dateofreceipt = dateofreceipt
                            # membership_fee.payment_data = payment_data[count]
                            # membership_fee.paymenttype = paymenttype[count]
                            membership_fee.amount = 2600
                            membership_fee.paymentname = "Membership"
                            membership_fee.receipt_no = get_number
                            membership_fee.save()
                        for i in range(4):
                            if i == 0:
                                payment = PaymentDetails.objects.filter(booking_id = customers.id).aggregate(Sum('amount'))
                                if split_amount == payment :
                                    continue
                                paymentname = 'DownPayment'
                                status =1 
                            elif i ==1:
                                status = 3
                                paymentname = 'FirstInstallment'
                            elif i == 2:
                                status = 5
                                paymentname = 'SecondInstallment'
                            else:
                                status = 7
                                paymentname = 'ThridInstallment'

                        
                            if split_amount <= int(payment_total):
                                payment_total = payment_total - split_amount
                                
                            else:
                                paid_amt_bal = (split_amount - payment_total)+2600
                                
                                if paid_amt_bal >= int(paid_amount[count]):
                                    
                                    if paid_amt_bal > int(paid_amount[count])+2600:
                                        payment_name = 'Half'
                                        # print('paid_amount:',paid_amount)
                                        # print('payment_name:',payment_name)
                                        # print('paid_amt_bal:',paid_amt_bal)
                                        # print('Spilt:',paid_amt_bal)
                                    else:
                                        payment_name = 'Full'
                                        status +=1
                                    payments = PaymentDetails()
                                    payments.booking=book
                                    payments.payment_mode = payment_mode[count]
                                    payments.bank = bank[count]
                                    payments.branch = branch[count]
                                    payments.cheque_no = cheque_no[count]
                                    payments.transaction = transaction_id[count]
                                    payments.ddno=ddno[count]
                                    # payments.payment_data = payment_data[count]
                                    payments.dateofreceipt = dateofreceipt
                                    payments.paymentname =paymentname+' '+payment_name
                                    payments.amount = int(paid_amount[count])
                                    payments.receipt_no = get_number
                                    payments.save()
                                    book.payments_status = status
                                    book.total_paid_amount =int(book.total_paid_amount )+ int(paid_amount[count])
                                    # print('total:', paid_amount[count])
                                    # print('total:', book.total_paid_amount)
                                    book.save()
                                    break
                                else:
                                    payments = PaymentDetails()
                                    payments.booking=book
                                    payments.payment_mode = payment_mode[count]
                                    payments.bank = bank[count]
                                    payments.branch = branch[count]
                                    payments.cheque_no = cheque_no[count]
                                    payments.transaction = transaction_id[count]
                                    payments.ddno=ddno[count]
                                    #payments.payment_data = payment_data[count]
                                    payments.dateofreceipt = dateofreceipt
                                    payments.paymentname =paymentname
                                    payments.amount = int(paid_amt_bal)
                                    payments.receipt_no = get_number
                                    payments.save()
                                    book.payments_status = status
                                    book.total_paid_amount =int(book.total_paid_amount )+ int(paid_amount[count])
                                    book.save()
                                    paid_amount=int(paid_amount[count]) -int(paid_amt_bal)
                        messages.success(request,'Successfully Saved')
            except Bookings.DoesNotExist:
                messages.error(request,'Saved failed')
    difference = int(total_site_value) - int(payment_total)
    if difference <= 0:
        differ = 0
    else:
        differ = difference
    return render(request,'new_bookings/generate.html',{'customer': customers,'difference': differ,'active_bookings':active_bookings})

def ugdg(request):
    exective = User.objects.filter(role='Executive')
    customers = {}
    pltsizes = PlotSize.objects.all()
    active_bookings = Bookings.objects.filter(user__is_active=1).exclude(date_of_change__isnull=True).order_by('-created_on').all()
    
    try:
        if request.method == 'POST':
            action = request.POST.get('action')
            user_id = request.POST.get('user_id')
            seniority_id = request.POST.get('search_membername')
            
            if action == 'search_customer':
                if seniority_id == '':
                    messages.error(request, 'Please Enter the Seniority No')
                else:
                    try:
                        customers = Bookings.objects.get(seniority_id=seniority_id)
                    except Bookings.DoesNotExist:
                        messages.error(request, 'Invalid seniority ID.')
            elif action == 'create_order':
                seniority = request.POST.get('seniority_id')
                book = Bookings.objects.get(user_id=user_id, seniority_id=seniority)
                project_id = request.POST.get('projectname')
                str_form = request.POST.get('selectDimension')
                str_to = request.POST.get('plotsize')
                
                land_detail = LandDetails.objects.get(project_id=project_id, plotsize_id=str_to)
                old_land_detail = LandDetails.objects.get(project_id=project_id, plotsize_id=str_form)
                
                   
                book.date_of_change = request.POST.get('date_of_change')
                book.type_of_change = request.POST.get('type_of_change')
                book.diff = request.POST.get('diff')
                executive_id = request.POST.get('executive')
                print(executive_id)
                value = User.objects.get(id=executive_id)
                get_execute = Executive.objects.get(user_id=value.id)    
                book.executive = value
                book.team_lead = request.POST.get('team_lead')
                book.sr_team_lead = request.POST.get('sr_team_lead')
                book.project_lead = request.POST.get('project_lead')
                book.type_bkg = request.POST.get('type_bkg')
                book.indvl_paid = request.POST.get('indvl_paid')
                book.tl_paid = request.POST.get('tl_paid')
                book.stl_paid = request.POST.get('stl_paid')
                book.PMname = request.POST.get('PMname')
                book.old_land_details = old_land_detail
                book.land_details = land_detail
                book.save()
                messages.success(request, 'Successfully Saved')
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
    
    return render(request, 'new_bookings/ugdg.html', {
        'pltsizes': pltsizes,
        'customer': customers,
        'exective': exective,
        'active_bookings':active_bookings
    })

def transfer(request):
    customers = {}
    user = {}
    active_bookings = Bookings.objects.filter(user__is_active=1).exclude(date_of_transfer__isnull=True).order_by('-created_on').all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        seniority_id = request.POST.get('search_membername')
        
        try:
            if action == 'search_customer':
                customers = Bookings.objects.get(seniority_id=seniority_id)
                user = User.objects.get(id=user_id)
                if not customers:
                    messages.error(request, 'Invalid Customer ID.')
            elif action == 'create_order':
                seniority = request.POST.get('seniority')
                user_id = request.POST.get('user_id')
                old_book = Bookings.objects.get(user_id=user_id, seniority_id=seniority)
                old_book.status = 0
                land_details_id = old_book.land_details_id
                
                book = Bookings()
                book.old_seniority_id = seniority
                book.user_id = user_id
                book.membership_id = request.POST.get('new_seniority')
                book.seniority_id = request.POST.get('new_seniority')
                book.date_of_transfer = request.POST.get('date_of_transfer')
                book.type_of_transfer = request.POST.get('type_of_transfer')
                book.affidavit = request.POST.get('affidavit')
                book.death_cert = request.POST.get('death_cert')
                book.total_site_value = old_book.total_site_value
                book.downpayment = old_book.downpayment
                book.land_details_id = land_details_id
                book.save()
                old_book.save()
                messages.success(request, 'Successfully updated')
        except Bookings.DoesNotExist:
            messages.error(request, 'Invalid seniority ID.')
        except User.DoesNotExist:
            messages.error(request, 'No user found for the given User ID')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')
    
    return render(request, 'new_bookings/transfer.html', {'customer': customers, 'user': user,'active_bookings':active_bookings})

def get_team_owner(request):
    if request.method == "POST":
        print ("Hi")
        id = request.POST.get('id','').strip()
        teamlead = User.objects.filter(role = 'Executive')
        details = TeamLead.objects.get(id=id)
        return JsonResponse({"values":list(teamlead),'shortcut':details.shortcode})
    return JsonResponse({})
    
def site_visit(request):
    visits = Site_visit.objects.all().order_by('-id')
    exective = User.objects.filter(role='Executive')
    detail = {}
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        try:
            if action == 'create_order':
                exective_id = request.POST.get('executive')
                value = User.objects.get(id=exective_id)
                get_execute = Executive.objects.get(user_id=value.id)
                teamlead = get_execute.teamlead.user.id
                senior_teamlead = get_execute.teamlead.sr_team.user.id
                project_lead = get_execute.teamlead.sr_team.project_head.id

                Site_visit(
                    date_of_site_visit=request.POST.get('date_of_visit'),
                    cust_name=request.POST.get('cust_name'),
                    phone_no=request.POST.get('phone_no'),
                    executive=value,
                    team_lead_id=teamlead,
                    proj_head_id=project_lead,
                    so_done_by=request.POST.get('so_done_by'),
                    sv_don_by=request.POST.get('sv_done_by'),
                    sv_category=request.POST.get('sv_category'),
                    source=request.POST.get('source'),
                    booked_no=request.POST.get('booked_no'),
                    booked_sry_no=request.POST.get('booked_sry_no'),
                    sv_status=request.POST.get('sv_status'),
                    PMname=request.POST.get('PMname'),

                ).save()

                messages.success(request, 'Successfully Saved')
        except User.DoesNotExist:
            messages.error(request, 'Executive not found for the given ID')
        except Executive.DoesNotExist:
            messages.error(request, 'Executive details not found for the given ID')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'new_bookings/site_visit.html', {'customer': detail, 'exective': exective,'visits':visits})

def view_site_visit(request):
    visits = Site_visit.objects.all().order_by('-id')
    
    if request.method == 'POST':
        try:
            for visit in visits:
                visit.date_of_site_visit = request.POST.get('date_of_visit')
                visit.cust_name = request.POST.get('cust_name')
                visit.phone_no = request.POST.get('phone_no')
                visit.executive = request.POST.get('executive')
                visit.so_done_by = request.POST.get('so_done_by')
                visit.sv_don_by = request.POST.get('sv_done_by')
                visit.sv_category = request.POST.get('sv_category')
                visit.source = request.POST.get('source')
                visit.booked_no = request.POST.get('booked_no')
                visit.booked_sry_no = request.POST.get('booked_sry_no')
                visit.sv_status = request.POST.get('sv_status')
                visit.PMname = request.POST.get('PMname')
                visit.save()
            
            messages.success(request, 'Successfully updated')
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'display/view_site_visit.html', {'visits': visits})

def update_site_visit(request, id):
    try:
        update = Site_visit.objects.get(id=id)
        
        if request.method == 'POST':
            exective = request.POST.get('executive')
            value = User.objects.get(id=exective)
            executive = User.objects.get(id=exective)
            executive_details = Executive.objects.get(user=executive)
            get_execute = Executive.objects.get(user_id=value.id)
            teamlead = get_execute.teamlead.user.id
            senior_teamlead = get_execute.teamlead.sr_team.user.id
            project_lead = get_execute.teamlead.sr_team.project_head.id
            
            update.date_of_site_visit = request.POST.get("date_of_visit")
            update.cust_name = request.POST.get("cust_name")
            update.phone_no = request.POST.get("phone_no")
            update.executive = executive
            update.so_done_by = request.POST.get("so_done_by")
            update.sv_don_by = request.POST.get("sv_done_by")
            update.sv_category = request.POST.get("sv_category")
            update.source = request.POST.get("source")
            update.booked_no = request.POST.get("booked_no")
            update.booked_sry_no = request.POST.get("booked_sry_no")
            update.sv_status = request.POST.get('sv_status')
            update.save()
            messages.success(request, 'Successfully updated')
            return redirect('/members/view_site_visit')
    
    except Site_visit.DoesNotExist:
        messages.error(request, 'Site visit not found for the given ID')
        return redirect('/members/view_site_visit')
    
    except User.DoesNotExist:
        messages.error(request, 'User not found for the given ID')
        return redirect('/members/view_site_visit')
    
    except Executive.DoesNotExist:
        messages.error(request, 'Executive details not found for the given ID')
        return redirect('/members/view_site_visit')
    
    except Exception as e:
        messages.error(request, f'An error occurred: {e}')
        return redirect('/members/view_site_visit')

    return render(request, 'display/update_display/update_site_view.html', {'update': update})

def delete_site_visit(request,id):
    deletesitevisit=Site_visit.objects.get(id=id)
    deletesitevisit.delete()
    # if delete.user-id.is_active == True:
    #     delete.user_id.is_active=False
    #     delete.user_id.save()  # Save the changes to the user object
        
    #     # Delete the site visit
    #     delete.delete()
    # context={
    #     'delete':delete,
    # }
    
    return redirect('/members/view_site_visit')

def lead_owner(request):
    exective = User.objects.filter(role = 'Executive')
    customers = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
            except Bookings.DoesNotExist:
                messages.error(request, 'Invalid seniority ID. ')
                customers = {}
                print('Muthu')
        elif action == 'create_order':
            user_id = request.POST.get('user_id')
            user_instance = User.objects.get(id=user_id)
         
            Leadowner(
                seniorityno_id = request.POST.get('seniority'),
                user_id = user_instance,
                executive = request.POST.get('executive'),
                team_lead = request.POST.get('team_lead'),
                sr_team_lead =request.POST.get('sr_team_lead'),
                project_head = request.POST.get('project_head'),
                type_of_booking = request.POST.get('type_of_booking'),
                ref_exis_cust_sry = request.POST.get('ref_exis_cust_sry'),
                ref_exis_cust_name = request.POST.get('ref_exis_cust_name'),
                date_of_sitevisit = request.POST.get('date_of_sitevisit'),
                sv_done_cust = request.POST.get('sv_done_cust'),
                source = request.POST.get('source'),
                id_card_status = request.POST.get('id_card_status'),
                fup_category = request.POST.get('fup_category'),
                install_fup_status = request.POST.get('install_fup_status'),
                install_fup_date = request.POST.get('install_fup_date'),
                exep_category = request.POST.get('exep_category'),
                excep_reason = request.POST.get('excep_reason'),
              
            ).save()
            messages.success(request, 'Successfully Saved')
    return render(request,'new_bookings/lead_owner.html',{'customer':customers,'exective':exective})

def cancel(request):
    customers = {}   
    active_bookings = Bookings.objects.filter(user__is_active=1).exclude(date_of_cancel__isnull=True).order_by('-date_of_cancel').all()
      
    if request.method == 'POST':
        action = request.POST.get('action')
        seniority_id = request.POST.get('search_membername')
        user_id = request.POST.get('user_id')

        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                if not customers:
                    messages.error(request, 'Invalid seniority ID.')
            except Bookings.DoesNotExist:
                customers = {}
                messages.error(request, 'Invalid seniority ID.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')
                
        elif action == 'create_order': 
            try:
                user_id = user_id
                seniority = request.POST.get('seniority')
                book = Bookings.objects.get(user_id=user_id, seniority_id=seniority)
                book.status = 0
                book.date_of_cancel = request.POST.get('date_of_cancel')
                book.type_of_cancel = request.POST.get('type_of_cancel')
                book.date_of_refund = request.POST.get('date_of_refund')
                book.mode_of_refund = request.POST.get('mode_of_refund')
                book.refund_cheque_no = request.POST.get('refund_cheque_no')
                book.refund_amount = request.POST.get('refund_amount')
                book.type_of_refund = request.POST.get('type_of_refund')
                book.issued_by = request.POST.get('issued_by')
                book.save()
                messages.success(request, 'Booking canceled successfully.')
            except Bookings.DoesNotExist:
                messages.error(request, 'No booking found for the given user and seniority ID.')
            except Exception as e:
                messages.error(request, f'Failed to cancel booking: {e}')

    return render(request, 'new_bookings/cancel.html', {'customer': customers,'active_bookings':active_bookings})

def receipts(request):
    distinct_receipts = PaymentDetails.objects.values('receipt_no').distinct()
    booking= []
    for receipt in distinct_receipts:
        latest_payment = PaymentDetails.objects.filter(receipt_no=receipt['receipt_no']).first()
        booking.append(latest_payment)

    ds=booking.reverse()
    data = PaymentDetails.objects.all()
    total_amount_per_receipt = defaultdict(int)
    for detail in data:
        total_amount_per_receipt[detail.receipt_no] += int(float(detail.amount))
    for receipt_no, total_amount in total_amount_per_receipt.items():
        print("Receipt No:", receipt_no, "Total Amount:", total_amount)   
    context = {
        'booking': booking,
        'total_amount_per_receipt': total_amount_per_receipt.items(),
      
    }
    return render(request,'view/receipts.html',context) 

def update_receipts(request, id):
    try:
        update_receipts = PaymentDetails.objects.filter(booking=id).last()
        if not update_receipts:
            messages.error(request, 'No payment details found for the given booking ID.')
            return redirect("/members/receipt")  # Redirect to a relevant page or handle this case appropriately
        
        if request.method == "POST":
            update_receipts.booking.user.first_name = request.POST.get('first_name', '')
            update_receipts.dateofreceipt = request.POST.get('dateofreceipt', '')
            update_receipts.branch = request.POST.get('branch', '')
            update_receipts.paymentname = request.POST.get('paymentname', '')
            update_receipts.payment_data = request.POST.get('payment_data', '')
            update_receipts.receipt_no = request.POST.get('receipt_no', '')
            update_receipts.booking.seniority_id = request.POST.get('seniority_id', '')
            update_receipts.booking.land_details.project.projectname = request.POST.get('projectname', '')
            update_receipts.amount = request.POST.get('amount', '')
            update_receipts.bank = request.POST.get('bank', '')
            update_receipts.payment_mode = request.POST.get('payment_mode', '')
            update_receipts.status = request.POST.get('status', '')

            if update_receipts.payment_mode == 'cheque':
                update_receipts.cheque_no = request.POST.get('cheque_no', '')
            elif update_receipts.payment_mode == 'dd':
                update_receipts.ddno = request.POST.get('ddno', '')
            elif update_receipts.payment_mode == 'transaction':
                update_receipts.transaction = request.POST.get('transaction', '')

            update_receipts.save()
            messages.success(request, 'Receipt details updated successfully.')
            return redirect("/members/receipt")

    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')

    return render(request, 'view/update_view/update_receipt.html', {'update_receipts': update_receipts})

def view_receipt(request,id):
    payment = PaymentDetails.objects.filter(booking=id).last()
    payments = PaymentDetails.objects.filter(booking=id)
   
    return render(request,'view/view_history.html',{'payment':payment,'payments':payments})

def btmt(request):
    project = Project.objects.all()
    context={
        'project':project
    }
    if request.method =="POST":
        data=Btmt()
        data.transaction_particulars = request.POST.get('transaction')
        data.cheque_no = request.POST.get('Chequeno')
        data.statemnt_amount = request.POST.get('stmtamount')
        data.date_of_credit = request.POST.get('creditdate')
        data.trans_category = request.POST.get('transcategory')
        data.trans_amount = request.POST.get('transamount')
        data.receipt_no = request.POST.get('receiptno')
        data.cr_dr_Code = request.POST.get('Cr/Dr_code')
        data.code_description = request.POST.get('codedescription')
        data.seniority_no = request.POST.get('seniority_no')
        data.amt_remark = request.POST.get('project_lead')
        data.project = request.POST.get('projectname')
        data.save()
        messages.success(request,'Successfully Saved')

    return render(request,'new_bookings/btmt.html',context)

from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

def activemember(request):
   
    active_users = UserDetail.objects.filter(user__is_active=1).all()
    active_nominees = UserNominee.objects.filter(user__is_active=1).all()
    active_bookings = Bookings.objects.filter(user__is_active=1).order_by('-created_on').all()
    different = 0  
    for booking in active_bookings:
        try:
            userdetail = UserDetail.objects.get(user_id=booking.user.id)
            booking.cus_dob = userdetail.dob
            booking.id_status = userdetail.id_card
            booking.email = userdetail.email
            booking.pan_no = userdetail.panno
            booking.pro_img = userdetail.profile
            booking.adhar_no = userdetail.aadhhaarno
            booking.last_n = booking.user.last_name
            nominee = active_nominees.get(user_id=booking.user.id)
            booking.nomie_name = nominee.nominee_name
            booking.nomie_age = nominee.nominee_age
            booking.nomie_rel = nominee.nominee_relationship
            booking.nomie_adrs = nominee.address
            booking.families = UserFamilyDetails.objects.filter(user_id=booking.user.id)
            for family in booking.families:
                print(family.member_age)
                print(family.member_relation)
        except ObjectDoesNotExist:
            pass
        bookings = Bookings.objects.all()
        for booking in bookings:
            different = int(booking.total_site_value) - int(booking.total_paid_amount)
           
    context = {
        'user': active_users,
        'book': active_bookings,
        'nomiee': active_nominees,
        'different': different  
    }
    
    return render(request, 'view/activemem.html', context)


def updateactivememberlist(request, id):
    try:
        user = User.objects.get(id=id)
        book = Bookings.objects.get(user=user)
        userdetail = UserDetail.objects.get(user=user)
        formatted_date = book.date_of_booking.strftime("%d-%m-%Y")

        if request.method == 'POST':
            user.first_name = request.POST.get("first_name", "")
            user.mobile_no = request.POST.get('mobile_no', "")
            user.save()

            book.seniority_id = request.POST.get('seniority_id', "")
            book.am_no = request.POST.get('am_no', "")
            book.save()

            userdetail.alternate_no = request.POST.get('alternate_no', "")
            userdetail.email = request.POST.get()("email","")
            userdetail.address = request.POST.get('address', "")
            userdetail.city = request.POST.get('city', "")
            userdetail.pincode = request.POST.get('pincode', "")
            userdetail.state = request.POST.get('state', "")
            userdetail.id_card = request.POST.get('id_card', "")
            userdetail.save()
        
            return redirect('/members/activemember')

        context = {
            'user': user,
            'book': book,
            'formatted_date': formatted_date,
            'userdetail': userdetail
        }
        return render(request, 'view/update_view/update_acmember.html', context)

    except User.DoesNotExist:
        # Handle case where user does not exist
        return render(request, 'view/update_view/update_acmember.html', {'error_message': 'User does not exist.'})
    except Bookings.DoesNotExist:
        # Handle case where bookings do not exist
        return render(request, 'view/update_view/update_acmember.html', {'error_message': 'Bookings do not exist.'})
    except UserDetail.DoesNotExist:
        # Handle case where user detail does not exist
        return render(request, 'view/update_view/update_acmember.html', {'error_message': 'User detail does not exist.'})
    except Exception as e:
        # Handle any other unexpected exceptions
        return render(request, 'view/update_view/update_acmember.html', {'error_message': f'An error occurred: {str(e)}'})

  
def deleteactivememberlist(request,id):
    book = Bookings.objects.get(user_id=id)
    if book.user.is_active == True:
        book.user.is_active=False
        book.user.save()
    context={
        'user':book,
    }
    
    return redirect('/members/activemember',context)
   

def update_personal(request,id):
    nomine =  UserNominee.objects.get(user_id=id)
    family_details =  UserFamilyDetails.objects.filter(user_id=id)
    card_details = UserDetail.objects.get(user_id=id)
    print('Addcard',card_details.panno)
    print('Addcard',card_details.aadhhaarno)
    if request.method =='POST':
        card_details.aadhhaarno = request.POST.get('aadhhaarno')
        card_details.panno = request.POST.get('panno')
        profile = request.POST.get('profile')
        if profile:
            card_details.profile = profile
        card_details.save()
        nomine.nominee_name = request.POST.get('nominee_name')
        nomine.nominee_age = request.POST.get('nominee_age')
        nomine.nominee_relationship = request.POST.get('nominee_relationship')
        nomine.address = request.POST.get('address')
        nomine.save()
        check_input_no = 1
        if check_input_no is not None:
            for family in family_details: 
                member_name_key = f'member_name{family.id}'        
                member_age_key = f'member_age{family.id}'
                member_relation_key = f'member_relation{family.id}'

                family.user_id= id
                family.member_name = request.POST.get(member_name_key)
                family.member_age = request.POST.get(member_age_key)
                family.member_relation = request.POST.get(member_relation_key)
                family.save()
        return redirect('/members/activemember')

    context={
        'card_details':card_details,
        'nomine':nomine,
        'family_details':family_details
    }
    return render(request,'view/update_view/update_personal.html',context)
def inactivemember(request):
    try:
        book1 = Bookings.objects.filter(user__is_active=0).all()
        user = User.objects.filter(is_active=True).all()
    except Exception as e:
       
        print(f"An error occurred: {e}")
       
        return render(request, 'error.html', {'error_message': 'An error occurred while fetching data.'})

    return render(request, 'view/inactivemem.html', {'book1': book1, 'user': user})

def update_inactive(request,id):
    book = Bookings.objects.get(id=id)
    if book.user.is_active == False:
        book.user.is_active=True
        book.user.save()
    return redirect('/members/inactivemember')

def confirmletter(request):
    try:
        user = Bookings.objects.order_by('-created_on').all()
    except Exception as e:
       
        print(f"An error occurred: {e}")
      
        return render(request, 'error.html', {'error_message': 'An error occurred while fetching data.'})

    return render(request, 'view/confirmleter.html', {'user': user})

def view_history(request):
    return render(request,'display/view_history.html')

def user_access(request, id):
    try:
        user_log = User.objects.get(id=id)
        
    except ObjectDoesNotExist:
        
        return render(request, 'error.html', {'error_message': 'User does not exist.'})
    except Exception as e:
        # Handle any other unexpected exceptions
        return render(request, 'error.html', {'error_message': f'An error occurred: {str(e)}'})

    if request.method == "POST":
        try:
            user_log.first_name = request.POST.get('first_name', '')
            user_log.last_name = request.POST.get('last_name', '')
            user_log.employee_id = request.POST.get('employee_id', '')
            user_log.role = request.POST.get('user_role', '')
            user_log.email = request.POST.get('email_id', '')
            user_log.mobile_no = request.POST.get('mobile_no', '')
            user_log.date_joined = request.POST.get('date_joined', '')
            user_log.save()
            return redirect('/members/view_user_access')
        except Exception as e:
            # Handle any errors that occur during saving user data
            return render(request, 'error.html', {'error_message': f'Failed to update user: {str(e)}'})

    return render(request, 'input/update_user/user_access.html', {'user_log': user_log})

def view_user_access(request):
    view_user=User.objects.filter(is_active=1).exclude(role__iexact="customer").order_by('-date_joined')
    messages.success(request, 'Successfully updated')
    return render(request,'input/update_user/view_user_access.html',{'view_user':view_user})

def delete_user_access(request, id):
    print(id)
    book = User.objects.get(id=id)
    print(book)
    if book.is_active == True:
        book.is_active=False
        book.save()

    context={
        'book':book,
    }

    return redirect(view_user_access)

def rate_update(request):
    return render(request,'input/update_rate/rate_update.html')

def view_rate_update(request):
    projects = Bookings.objects.all()
    return render(request,'input/update_rate/view_rate_update.html',{'projects':projects})

def update_sales_staff(request):
    return render(request,'input/update_sales_staff/update_staff.html')

def view_update_sales_staff(request):
    return render(request,'input/update_sales_staff/view_update_staff.html')

def blocked_seniority(request):
    if request.method == 'POST':
        Update_blocked(
            project=request.POST['project'],
            seniority_no=request.POST['seniority_no'],
            blocked_date=request.POST['blocked_date'],
            executive=request.POST['executive'],
            customer_name=request.POST['customer_name'],
        ).save()
        messages.success(request, 'Successfully Saved')
    return render(request,'input/blocked_update/block_seniority.html')

def view_blocked_seniority(request):
    view_block=Update_blocked.objects.filter(is_active=1)
    return render(request,'input/blocked_update/view_block_seniority.html',{'view_block':view_block})

def update_block(request,id):
    block_update=Update_blocked.objects.get(id=id)
    print('1','Hello')
    if request.method == "POST":         
        block_update.project = request.POST['project']
        block_update.seniority_no = request.POST['seniority_no'] 
        block_update.blocked_date = request.POST['blocked_date']
        block_update.executive = request.POST['executive']
        block_update.customer_name = request.POST['customer_name']
        block_update.save() 
        messages.success(request, 'Successfully updated')
        print('2','Hello')
        return redirect('/members/view_blocked_seniority')
    return render(request,'input/blocked_update/update_block.html',{'block_update':block_update})

def delete_block(request, id):
    book = Update_blocked(id=id)
    if book.is_active:
        book.is_active = False
        book.save()
    return redirect('view_blocked_seniority')

def update_pdc(request):
    
    return render(request,'input/pdc/update_pdc.html')

def view_call_request(request):
    view_call_request = Request_call.objects.all()
    return render(request,'image/callrequest.html',{"view_call_request":view_call_request})

def view_update_pdc(request):
    view_update_pdc = pdc_update.objects.all()
    return render(request,'input/pdc/view_update_pdc.html',{"view_update_pdc":view_update_pdc})

def cr_code(request):
     return render(request,'input/cr_code/update_cr_code.html')
