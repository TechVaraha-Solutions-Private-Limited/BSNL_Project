from django.shortcuts import render
from django.http import JsonResponse
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee
from .models import Bookings,PaymentDetails,Ugdg,Receipts
from dashboard.projects.models import Project,PlotSize,LandDetails
from django.forms.models import model_to_dict
# Create your views here.
def home(request):
    return render(request,'common/index.html')

def add_new_bookings(request):
    data = LandDetails.objects.all()
    projects = Project.objects.all()
    # landsize = PlotSize.objects.filter()
    # landdetail = LandDetails.objects.get(projectname=project, plotsize=landsize)
    landdetail = LandDetails.objects.all()
    if request.method=='POST':
        user=User()
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.mobile_no = request.POST.get('mobile_no')
        user.email = request.POST.get('email')
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

        book = Bookings()
        book.user = user
        book.project = request.POST.get('projectname')
        book.seniority_id = request.POST.get('seniority_id')
        book.dimension = request.POST.get('dimension')
        book.total_site_value = request.POST.get('total_site_value')
        book.downpayment = request.POST.get('downpayment')
        book.site_refer = request.POST.get('site_refer')
        book.save()

        payments = PaymentDetails()
        payments.booking=book
        payments.payment_mode = request.POST.get('payment_mode')
        payments.bank = request.POST.get('bank')
        payments.branch = request.POST.get('branch')
        payments.cheque_no = request.POST.get('cheque_no')
        payments.payment_data = request.POST.get('payment_data')
        payments.amount = request.POST.get('amount')
        payments.am_no = request.POST.get('am_no')
        payments.receipt_no = request.POST.get('receipt_no')
        payments.save()
    
    return render(request, 'new_bookings/add_new_bookings.html',{'landdetail':data,'projects':projects})

def get_dimension(request):
    if request.method == "POST":
        id = request.POST.get('id','').strip()
        dimensions = PlotSize.objects.filter(landdetails__project=id).values()
        return JsonResponse({"values":list(dimensions)})
    return JsonResponse({})
def booksum(request):
    return render(request,'home/booksum.html')

def bss(request):
    return render(request,'home/bss.html')

def generate(request):
    selected_customer = None
    order_created = False
    matching_customers = []
    username = None 

    if request.method == 'POST':
        action = request.POST.get('action')
        print('aution:',action)

        if action == 'search_customer':
            seniority_id = request.POST.get('search_membername')
            print('Search seniority_id:', seniority_id)
            

            customers = Bookings.objects.filter(seniority_id=seniority_id)
            print('Search seniority_id:', seniority_id)
            if customers.exists():
                matching_customers = customers

        elif action == 'create_order':
            seniority_id = request.POST.get('search_membername')

            customer = Bookings.objects.get(seniority_id=seniority_id)
           
            username = request.POST.get('username')
            seniority_id = seniority_id
            amount = request.POST.get('amount')
            modeofpay = request.POST.get('modeofpay')
            chequeno = request.POST.get('chequeno')
            bank = request.POST.get('bank')
            branch = request.POST.get('branch')
            paydate = request.POST.get('paydate')
            paystatus = request.POST.get('paystatus')
            dateofreceipt = request.POST.get('dateofreceipt')

            try:
               
                print('cust',customer)

                # Create a new order instance
                order = PaymentDetails(
                    username=username,
                    seniority_id = customer.seniority_id,
                    amount=amount,
                    modeofpay=modeofpay,
                    chequeno=chequeno,
                    bank=bank,
                    branch=branch,
                    paydate=paydate,
                    paystatus=paystatus,
                    dateofreceipt=dateofreceipt
                )
                print('or:',order)
                order.save()
                order_created = True

            except Bookings.DoesNotExist:
                print('failed')
    return render(request,'new_bookings/generate.html',{'selected_customer': selected_customer, 'order_created': order_created, 'matching_customers': matching_customers})

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
    return render(request,'view/receipts.html')

def btmt(request):
    return render(request,'new_bookings/btmt.html')

def activemember(request):
    user = User.objects.all()
    project =Project.objects.all()
    book = Bookings.objects.all()
    userdet = Receipts.objects.all()
    return render (request,'view/activemem.html',{'user':user,
                                                  'project':project,
                                                  'book':book,
                                                  'userdet':userdet})

def inactivemember(request):
    user = User.objects.all()
    project =Project.objects.all()
    book = Bookings.objects.all()
    userdet = Receipts.objects.all()
    return render (request,'view/inactivemem.html',{'user':user,
                                                  'project':project,
                                                  'book':book,
                                                  'userdet':userdet})

def confirmletter(request):
    user=User.objects.all()
    userdet = Receipts.objects.all()
    project =Project.objects.all()
    return render(request,'view/confirmleter.html',{'user':user,
                                                    'userdet':userdet,
                                                    'project':project})

def view_history(request):
    return render(request,'display/view_history.html')

def user_access(request):
    return render(request,'input/update_user/user_access.html')

def view_user_access(request):
    return render(request,'input/update_user/view_user_access.html')

def rate_update(request):
    return render(request,'input/update_rate/rate_update.html')

def view_rate_update(request):
    return render(request,'input/update_rate/view_rate_update.html')

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