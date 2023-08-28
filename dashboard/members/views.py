from django.shortcuts import render
from dashboard.userinfo.models import User,UserDetail,UserFamilyDetails,UserNominee
from .models import Bookings,PaymentDetails

# Create your views here.

def add_new_bookings(request):
    if request.method=='POST':
        user=User()
        user.first_name=request.POST.get('first_name')
        user.last_name=request.POST.get('last_name')
        user.mobile_no = request.POST.get('mobile_no')
        user.email = request.POST.get('email')
        user.is_password_set = request.POST.get('password')
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
        # book = Bookings()
        # book.project = request.POST.get('project')
        # book.seniority_id = request.POST.get('seniority_id')
        # book.membership_id = request.POST.get('membership_id')
        # book.save()

        # payments = PaymentDetails()
        # payments.booking=book
        # payments.payment_mode = request.POST.get('payment_mode')
        # payments.bank = request.POST.get('bank')
        # payments.branch = request.POST.get('branch')
        # payments.cheque_no = request.POST.get('cheque_no')
        # payments.payment_data = request.POST.get('payment_data')
        # payments.amount = request.POST.get('amount')
        # payments.save()
    return render(request, 'new_bookings/add_new_bookings.html')

def booksum(request):
    return render(request,'home/booksum.html')

def bss(request):
    return render(request,'home/bss.html')