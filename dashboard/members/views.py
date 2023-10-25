from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee
from .models import Bookings,PaymentDetails,Ugdg,Receipts,Images,Leadowner,Site_visit
from dashboard.projects.models import Project,PlotSize,LandDetails
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.hashers import make_password
# Create your views here.
def banner_images(request):
    if request.method =='POST':
        Images(
            images=request.POST['profile'],
            place = "Banner"
        ).save()        
    return render(request,'image/banner.html')

def home(request):
    return render(request,'common/index.html')

def addcustomer(request):
    if request.method == "POST":
        first_name=request.POST.get('first_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        email_is_exit = User.objects.filter(email=email).exists()|User.objects.filter(mobile_no=mobile_no).exists()
        if not first_name :
            messages.error(request,'Enter the Name')
        elif email_is_exit:
            messages.error(request,'E-mail Already Exists')
        else:
            user=User()
            user.first_name=first_name
            user.last_name=request.POST.get('last_name')
            user.mobile_no = mobile_no
            user.email = email
            user.password = make_password(request.POST.get('password','').strip())
            user.role = "Customer"
            user.save()
            details = UserDetail()
            details.user = user
            details.dob = request.POST.get('dob')
            details.age = request.POST.get('age')
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

def add_new_bookings(request):
    projects = Project.objects.all()
    landdetail = LandDetails.objects.all()
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        email = request.POST.get('email')
        mobile_no = request.POST.get('mobile_no')
        seniority_id = request.POST.get('seniority_id')
        seniority_id_is_exit =Bookings.objects.filter(seniority_id=seniority_id).exists()
        email_is_exit = User.objects.filter(email=email).exists()|User.objects.filter(mobile_no=mobile_no).exists()
        if not first_name :
            messages.error(request,'Enter the Name')
        elif email_is_exit:
            messages.error(request,'E-mail Already Exists')
        elif seniority_id_is_exit:
            messages.error(request,'Seniority Already Exists')
        else:
            user=User()
            user.first_name=first_name
            user.last_name=request.POST.get('last_name')
            user.mobile_no = mobile_no
            user.email = email
            user.password = make_password(request.POST.get('password','').strip())
            user.role = "Customer"
            user.save()
            details = UserDetail()
            details.user = user
            details.dob = request.POST.get('dob')
            details.age = request.POST.get('age')
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
            book.am_no = auto_genrate
            book.save()
            #vicky
            get_number = PaymentDetails.objects.all().order_by('-id')[:1]
            if get_number:
                get_number = "B-" + str(get_number[0].id + 1).zfill(5)
            else:
                get_number = "B-00001"             
            payments = PaymentDetails()
            payments.booking=book
            payments.payment_mode = request.POST.get('payment_mode')
            payments.bank = request.POST.get('bank')
            payments.branch = request.POST.get('branch')
            payments.cheque_no = request.POST.get('cheque_no')
            payments.user = user
            payments.payment_data = request.POST.get('payment_data')
            payments.amount = request.POST.get('amount')
            payments.receipt_no = get_number
            payments.save()
            messages.error(request,'Successfully Saved')
            # Vicky    
    return render(request, 'new_bookings/add_new_bookings.html',{'landdetail':landdetail,'projects':projects})

def get_dimension(request):
    if request.method == "POST":
        id = request.POST.get('id','').strip()
        dimensions = PlotSize.objects.filter(landdetails__project=id).values()
        return JsonResponse({"values":list(dimensions)})
    return JsonResponse({})

def get_project_value(request):
    print('hello')
    if request.method == "POST":
        project_id = request.POST.get('project_id','').strip()
        plot_id = request.POST.get('plot_id','').strip()
        id = request.POST.get('project_id','').strip()
        dimensions = LandDetails.objects.filter(project_id=project_id,plotsize_id=plot_id).values()
        return JsonResponse({"values":list(dimensions)})
    return JsonResponse({})

def get_project_id(request):
    if request.method == "POST":
        plot_id = request.POST.get('plot_id','').strip()
        dimensions = LandDetails.objects.filter(landdetails__project=plot_id).values()
        print(dimensions)
        return JsonResponse({"values":list(dimensions)})
    return JsonResponse({})

def booksum(request):
    return render(request,'home/booksum.html')

def bss(request):
    return render(request,'home/bss.html')

def print_receipt(request):
    return render('reports/print_recepit.html')

def generate(request):
    customers = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                
                if customers =='':
                    messages.error(request, 'Profile details updated.')
            except:
                customers = {}       
        elif action == 'create_order':
            seniority = request.POST.get('seniority_id')
            book = Bookings.objects.get(user_id=user_id,seniority_id=seniority)
            PaymentDetails()
            try:
                # Create a new order instance
                get_number = PaymentDetails.objects.all().order_by('-id')[:1]
                if get_number:
                    get_number = "B-" + str(get_number[0].id + 1).zfill(5)
                else:
                    get_number = "B-00001"
                order = PaymentDetails(
                    booking = book,
                    amount = request.POST.get('amount'),
                    dateofreceipt = request.POST.get('dateofreceipt'),
                    bank = request.POST.get('bank'),
                    branch = request.POST.get('branch'),
                    cheque_no = request.POST.get('chequeno'),
                    payment_data = request.POST.get('payment_data'),
                    receipt_no = get_number,
                    payment_mode = request.POST.get('modeofpay')
                )
                print('or:',order)
                order.save()
                print(order)
                messages.error(request,'Successfully Saved')
            except Bookings.DoesNotExist:
                print('failed')
    return render(request,'new_bookings/generate.html',{'customer': customers})

def ugdg(request):
    customers = {}
    pltsizes = PlotSize.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                if customers =='':
                    messages.error(request, 'Profile details updated.')
            except:
                customers = {}  
                
        elif action == 'create_order':
            seniority = request.POST.get('seniority_id')
            book = Bookings.objects.get(user_id=user_id,seniority_id=seniority)
            project_id = request.POST.get('projectname')
            str_form = request.POST.get('selectDimension')
            str_to = request.POST.get('plotsize')
            land_detail = LandDetails.objects.get(project_id=project_id,plotsize_id=str_to)
            old_land_detail = LandDetails.objects.get(project_id=project_id,plotsize_id=str_form)
            book.date_of_change = request.POST.get('date_of_change')
            book.type_of_change = request.POST.get('type_of_change')
            book.diff = request.POST.get('diff')
            book.exective = request.POST.get('executive')
            book.team_lead = request.POST.get('team_lead')
            book.sr_team_lead = request.POST.get('sr_team_lead')
            book.project_lead  = request.POST.get('project_lead')
            book.type_bkg = request.POST.get('type_bkg')
            book.indvl_paid =request.POST.get('indvl_paid')
            book.tl_paid =request.POST.get('tl_paid')
            book.stl_paid = request.POST.get('stl_paid')
            book.old_land_details = old_land_detail
            book.land_details = land_detail
            book.save()
        
    return render(request,'new_bookings/ugdg.html',{
            'pltsizes':pltsizes,
            'customer': customers
        })

def transfer(request):
    customers = {}
    user ={}
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                user=User.objects.get(id=user_id)
                print(user.first_name)
                if customers =='':
                    messages.error(request, 'Profile details updated.')
            except:
                customers = {}
                user={}
        elif action == 'create_order':
            seniority = request.POST.get('seniority')
            user_id = request.POST.get('user_id')
            print(seniority)
            old_book = Bookings.objects.get(user_id=user_id,seniority_id=seniority)
            old_book.status=0
            land_details_id = old_book.land_details_id
            book = Bookings()
            book.old_seniority_id = seniority
            book.user_id =user_id
            book.membership_id = request.POST.get('new_seniorty')
            book.seniority_id = request.POST.get('new_seniorty')
            book.date_of_transfer = request.POST.get('date_of_transfer')
            book.type_of_transfer = request.POST.get('type_of_transfer')
            book.affidavit = request.POST.get('affidavit')
            book.death_cert = request.POST.get('deathcerft')
            book.total_site_value = old_book.total_site_value
            book.downpayment = old_book.downpayment
            book.land_details_id = land_details_id
            book.save()
            old_book.save()

    return render(request,'new_bookings/transfer.html',{'customer':customers,'user':user})

def site_visit(request):
    customers = {}
    detail = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                detail = Leadowner.objects.get(seniorityno_id=seniority_id)
                if customers =='':
                    messages.error(request, 'Profile details updated.')
            except:
                customers = {}
                detail = {}
                print('Muthu')
        elif action == 'create_order':
            print('muthu')
            user_id = request.POST.get('user_id')
            user_instance= Leadowner.objects.get(seniorityno_id=seniority_id)
            # user_instance = Leadowner.objects.get(user_id=user_id)
            Site_visit(
                leadowner =user_instance,
                so_done_by = request.POST.get('so_done_by'),
                sv_don_by = request.POST.get('sv_done_by'),
                sv_category = request.POST.get('sv_category'),
                source = request.POST.get('source'),
                booked_no = request.POST.get('booked_no'),
                booked_sry_no = request.POST.get('booked_sry_no')
            ).save()
    return render(request,'new_bookings/site_visit.html',{'customer':detail})

def lead_owner(request):
    customers = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        seniority_id = request.POST.get('search_membername')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                
                if customers =='':
                    messages.error(request, 'Profile details updated.')
            except:
                customers = {}
                print('Muthu')
        elif action == 'create_order':
            user_id = request.POST.get('user_id')
            user_instance = User.objects.get(id=user_id)
            print('muthu')
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
                source = request.POST.get('sv_done_cust'),
                id_card_status = request.POST.get('id_card_status'),
                fup_category = request.POST.get('fup_category'),
                install_fup_status = request.POST.get('install_fup_status'),
                install_fup_date = request.POST.get('install_fup_date'),
                exep_category = request.POST.get('exep_category'),
                excep_reason = request.POST.get('excep_reason')
            ).save()
    return render(request,'new_bookings/lead_owner.html',{'customer':customers})

def cancel(request):
    customers = {}
    if request.method == 'POST':
        action = request.POST.get('action')
        seniority_id = request.POST.get('search_membername')
        user_id = request.POST.get('user_id')
        if action == 'search_customer':
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
                
                if customers =='':
                    messages.error(request, 'Profile details updated.')
            except:
                customers = {}
                print('Muthu')
        elif action == 'create_order': 
            user_id=user_id
            seniority = request.POST.get('seniority')
            book = Bookings.objects.get(user_id=user_id,seniority_id=seniority)
            book.status=0
            book.date_of_cancel =request.POST.get('date_of_cancel')
            book.type_of_cancel = request.POST.get('type_of_cancel')
            book.date_of_refund = request.POST.get('date_of_refund')
            book.mode_of_refund = request.POST.get('mode_of_refund')
            book.refund_cheque_no = request.POST.get('refund_cheque_no')
            book.refund_amount = request.POST.get('refund_amount')
            book.type_of_refund = request.POST.get('type_of_refund')
            book.issued_by = request.POST.get('issued_by')
            book.save()
    return render(request,'new_bookings/cancel.html',{'customer':customers})

def receipts(request):
    details = PaymentDetails.objects.all()
    return render(request,'view/receipts.html',{'details':details})   

def deletereceipts(request,id):
    details=PaymentDetails.objects.get(id=id)
    details.delete()
    return redirect(receipts)

def btmt(request):
    return render(request,'new_bookings/btmt.html')

def activemember(request):
    user = UserDetail.objects.filter(user__is_active=1).all()
    book = Bookings.objects.filter(user__is_active=1).all()   
    context={
        'user':user,
        'book':book,
    }
    return render (request,'view/activemem.html',context)

def updateactivememberlist(request,id):
    user =  User.objects.get(id=id)
    book = Bookings.objects.get(user=user)
    userdetail = UserDetail.objects.get(user=user)
    print("id:",userdetail)
    if request.method =='POST':
        user.first_name=request.POST.get("first_name")
        user.mobile_no = request.POST.get('mobile_no')
        user.save()
        book.seniority_id = request.POST.get('seniority_id')
        book.am_no = request.POST.get('am_no')
        book.created_on = request.POST.get('created_on')
        book.save()
        userdetail.alternate_no = request.POST.get('alternate_no')
        userdetail.address = request.POST.get('address')
        userdetail.city = request.POST.get('city')
        userdetail.state = request.POST.get('state')
        userdetail.save()
        return redirect('/members/activemember')
    context={
        'user':user,
        'book':book,
        'userdetail':userdetail
    }
    
    return render(request,'view/update_view/update_acmember.html',context)

def deleteactivememberlist(request,id):
    print("id:",id)
    book = Bookings.objects.get(id=id)
    print("id:",id,book.user.is_active)
    if book.user.is_active == True:
        book.user.is_active=False
        book.user.save()
    context={
        'user':book,
    }
    return redirect('/members/activemember',context)

def inactivemember(request):
    book1 = Bookings.objects.filter(user__is_active=0).all()
    user = User.objects.filter(is_active=True).all()
    return render (request,'view/inactivemem.html',{'book1':book1,'user':user})

def confirmletter(request):
    user=Bookings.objects.all()
    return render(request,'view/confirmleter.html',{'user':user})

def view_history(request):
    return render(request,'display/view_history.html')

def user_access(request):
    return render(request,'input/update_user/user_access.html')

def view_user_access(request):
    return render(request,'input/update_user/view_user_access.html')

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
    return render(request,'input/blocked_update/block_seniority.html')

def view_blocked_seniority(request):
    return render(request,'input/blocked_update/view_block_seniority.html')

def update_pdc(request):
    return render(request,'input/pdc/update_pdc.html')

def view_update_pdc(request):
    return render(request,'input/pdc/view_update_pdc.html')

def cr_code(request):
    return render(request,'input/cr_code/update_cr_code.html')

