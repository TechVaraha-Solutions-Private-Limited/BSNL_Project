from django.shortcuts import render,redirect, HttpResponse
from django.http import JsonResponse
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee
from .models import Bookings,PaymentDetails,Ugdg,Receipts
from dashboard.projects.models import Project,PlotSize,LandDetails
from django.forms.models import model_to_dict
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request,'common/index.html')

def add_new_bookings(request):
    projects = Project.objects.all()
    # landsize = PlotSize.objects.filter()
    # landdetail = LandDetails.objects.get(projectname=project, plotsize=landsize)
    get_last_number =  PaymentDetails.objects.all().order_by('-id')[:1]
    print(get_last_number[0].id)
    auto_genrate = str(get_last_number[0].id+1).zfill(5)

    am_auto = "AM-" +auto_genrate
    print(am_auto)

    get_number =  PaymentDetails.objects.all().order_by('-id')[:1]
    print(get_number[0].id)
    auto_genrate = str(get_number[0].id+1).zfill(5)
    recepit_auto = "B-" +auto_genrate
    print(recepit_auto)
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
            messages.error(request,'Mobile No or E-mail not correct')
        elif seniority_id_is_exit:
            messages.error(request,'Seniority Already Exists')
        else:
            user=User()
            user.first_name=first_name
            user.last_name=request.POST.get('last_name')
            user.mobile_no = mobile_no
            user.email = email
            user.password = request.POST.get('password')
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
        
            family = UserFamilyDetails()
            family.user = user
            family.member_name = request.POST.get('state1')
            family.member_age = request.POST.get('state1')
            family.member_relation = request.POST.get('state1')
            family.save()

            print(get_last_number[0].id)
            auto_genrate = str(get_last_number[0].id+1).zfill(5)
            am_auto = "AM-" +auto_genrate
            print(am_auto)
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
            book.am_no = am_auto
            book.save()
            #vicky
            get_last_number =  PaymentDetails.objects.all().order_by('-id')[:1]
            
            get_number =  PaymentDetails.objects.all().order_by('-id')[:1]
            print(get_number[0].id)
            auto_genrate = str(get_number[0].id).zfill(5)
            recepit_auto = "B-" +auto_genrate
            print(recepit_auto)

            payments = PaymentDetails()
            payments.booking=book
            payments.payment_mode = request.POST.get('payment_mode')
            payments.bank = request.POST.get('bank')
            payments.branch = request.POST.get('branch')
            payments.cheque_no = request.POST.get('cheque_no')
            payments.user = user
            payments.payment_data = request.POST.get('payment_data')
            payments.amount = request.POST.get('amount')
            payments.receipt_no = recepit_auto
            payments.save()


            messages.error(request,'Successfully Saved')
        #Vicky
        # payments
        # payments.id
        # generated_id = payments.id
        # am_auto = "AM-" +generated_id
       
    
    return render(request, 'new_bookings/add_new_bookings.html',{'landdetail':landdetail,'projects':projects})

def get_dimension(request):
    if request.method == "POST":
        id = request.POST.get('id','').strip()
        dimensions = PlotSize.objects.filter(landdetails__project=id).values()
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
    selected_customer = None
    order_created = False
    customers = {}
    user= None 

    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        seniority_id = request.POST.get('search_membername')
        print('aution:',action)
        if action == 'search_customer':
            
            print('Search seniority_id:', seniority_id)
            try:
                customers = Bookings.objects.get(seniority_id=seniority_id)
            except:
                customers = {}
                
        elif action == 'create_order':
            print("create order i am working")
            seniority = request.POST.get('seniority_id')
            print("create order i am working")
            print(user_id,seniority)
            book = Bookings.objects.get(user_id=user_id,seniority_id=seniority)
            PaymentDetails()
            # booking = book
            # amount = request.POST.get('amount')
            # dimension_id =request.POST.get('dimension')
            # dateofreceipt = request.POST.get('dateofreceipt')
            # bank = request.POST.get('bank')
            # branch = request.POST.get('branch')
            # cheque_no = request.POST.get('chequeno')
            # payment_data = request.POST.get('payment_data')
            # paystatus = request.POST.get('paystatus')
            # # payment_mode = request.POST.get('modeofpay')
            try:
                # Create a new order instance
                order = PaymentDetails(
                     booking = book,
                    amount = request.POST.get('amount'),
                    dateofreceipt = request.POST.get('dateofreceipt'),
                    bank = request.POST.get('bank'),
                    branch = request.POST.get('branch'),
                    cheque_no = request.POST.get('chequeno'),
                    payment_data = request.POST.get('payment_data'),
                    receipt_no = request.POST.get('receipt_no'),
                    payment_mode = request.POST.get('modeofpay')
                )
                print('or:',order)
                order.save()
                print(order)
                order_created = True
                messages.error(request,'Successfully Saved')
            except Bookings.DoesNotExist:
                print('failed')
    return render(request,'new_bookings/generate.html',{'selected_customer': selected_customer, 'order_created': order_created, 'customer': customers})

def ugdg(request):
    if request.method == 'POST':
        Ugdg(
            cut_name=request.POST.get['cust_name'],
            data_of_change = request.POST.get['date_of_change'],
            type_of_change = request.POST.get['type_of_change'],
            sft_form = request.POST.POST.get['sft_form'],
            sft_to = request.POST.get['sft_to'],
            diff = request.POST.get['diff'],
            executive = request.POST.get['executive'],
            team_lead = request.POST.get['team_lead'],
            sr_team_lead = request.POST.get['sr_team_lead'],
            project_lead  = request.POST.get['project_lead'],
            type_bkg = request.POST.get['type_bkg'],
            indvl_paid =request.POST.get['indvl_paid'],
            tl_paid =request.POST.get['tl_paid'],
            stl_paid = request.POST.get['stl_paid'],
        ).save()
        
    return render(request,'new_bookings/ugdg.html')

def transfer(request):
    return render(request,'new_bookings/transfer.html')

def site_visit(request):
    return render(request,'new_bookings/site_visit.html')

def lead_owner(request):
    return render(request,'new_bookings/lead_owner.html')

def cancel(request):
    return render(request,'new_bookings/cancel.html')

def receipts(request):
    details = PaymentDetails.objects.all()
    return render(request,'view/receipts.html',{'details':details})   

def deletereceipts(request,id):
    print ('id:',id)
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

