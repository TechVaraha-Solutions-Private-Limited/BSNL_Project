from django.shortcuts import render,redirect
from dashboard.members.models import Bookings,PaymentDetails
from dashboard.projects.models import Project
from dashboard.userinfo.models import UserDetail
from num2words import num2words
from django.db.models import Sum
# Create your views here.
def confirmletter_view(request,id):
    book=Bookings.objects.get(id=id)
    userdetail = UserDetail.objects.get(user=book.user)
    payment = PaymentDetails.objects.filter(booking=book)
    return render(request,'confirmletter_view.html',{'user':book,'userdetail':userdetail,'payment':payment})

def print_recepit(request,id):
    user=Bookings.objects.get(id=id)
    userdetail = UserDetail.objects.get(user=user.user)
    payments = PaymentDetails.objects.filter(booking_id=user.id)
    payment_count = PaymentDetails.objects.filter(booking_id=user.id).values('receipt_no').distinct().count()
    print(payment_count)
    for payment in payments:
        last_payment = payment.amount
        if last_payment:
            no = float(last_payment)
            receipt_no = num2words(no)
            print(receipt_no)
    get_last = PaymentDetails.objects.filter(booking_id=user.id).last()
    value = get_last.amount
    no = float(value)
    word1 = num2words(no, lang='en_IN')
    word = word1.replace(',','')
    print("132545",word)   
    context ={
        'user':user,
        'userdetail':userdetail,
        'payment':payments,
        'payment_count':payment_count,
        'word':word,
        'value':value,
    }
    return render (request,'print_recepit.html',context)

def booking_report(request):
    view_report = PaymentDetails.objects.all()
    project = Project.objects.all()
    for view in view_report:
        detail = UserDetail.objects.get(user_id = view.booking.user)
        view.userinfo = detail.alternate_no
        view.address = detail.address
        #print(view.booking.land_details.project.projectname)
    if request.method == 'POST':
        value = request.POST.get('projectOption')
        view_reports = PaymentDetails.objects.distinct()
        bookings = Bookings.objects.filter(land_details__project__projectname = value)
        #filter(booking__land_details__project__projectname=value)
        print(value)
        if value == 'all':
                print(value)
                bookings = Bookings.objects.all() 
                print(bookings)
        for booking in bookings:
            
            payments = booking.paymentdetails_set.all()
            booking.total_amt = payments.aggregate(Sum('amount'))['amount__sum']
            booking.address = UserDetail.objects.get(user_id = booking.user.id).address
            booking.alter = UserDetail.objects.get(user_id = booking.user.id).alternate_no
           
        context={
        'view_report': view_report,
        'project':project,
        'view_reports':view_reports,
        'bookings':bookings,
        }
        return render(request, 'booking_report.html', context)
    content={
        'project':project,
        
    }
    return render(request, 'booking_report.html',content)