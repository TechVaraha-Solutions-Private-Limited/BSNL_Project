from django.shortcuts import render,redirect,HttpResponse
from dashboard.members.models import Bookings,PaymentDetails,Site_visit
from dashboard.projects.models import Project
from dashboard.userinfo.models import UserDetail,Executive
from num2words import num2words
from django.db.models import Sum
from datetime import datetime, date, timedelta
import csv
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
    bookings =Bookings.objects.all()
    for view in view_report:
        detail = UserDetail.objects .get(user_id = view.booking.user)
        view.userinfo = detail.alternate_no
        view.address = detail.address

    if request.method == 'POST':
        data = request.POST.get('paymenttype')
        value = request.POST.get('projectOption')
        select = request.POST.get('reportType')
        print(data)
        if select == 'project':
            if value == 'all':
                bookings = Bookings.objects.all()
            else:
                bookings = Bookings.objects.filter(land_details__project__projectname = value)
            for booking in bookings:
                payments = booking.paymentdetails_set.all()
                booking.total_amt = payments.aggregate(Sum('amount'))['amount__sum']
                booking.address = UserDetail.objects.get(user_id = booking.user.id).address
                booking.alter = UserDetail.objects.get(user_id = booking.user.id).alternate_no
        elif select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                bookings = Bookings.objects.filter(created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   created_on__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
                for booking in bookings:
                    payments = booking.paymentdetails_set.all()
                    booking.total_amt = payments.aggregate(Sum('amount'))['amount__sum']
                    booking.address = UserDetail.objects.get(user_id = booking.user.id).address
                    booking.alter = UserDetail.objects.get(user_id = booking.user.id).alternate_no           
        elif select == 'project_head':
            bookings = Bookings.objects.filter(project_lead = value)
            for booking in bookings:
                payments = booking.paymentdetails_set.all()
                booking.total_amt = payments.aggregate(Sum('amount'))['amount__sum']
                booking.address = UserDetail.objects.get(user_id = booking.user.id).address
                booking.alter = UserDetail.objects.get(user_id = booking.user.id).alternate_no
            
        elif select == 'executive':
            bookings = Bookings.objects.filter(exective = value)
            for booking in bookings:
                payments = booking.paymentdetails_set.all()
                booking.total_amt = payments.aggregate(Sum('amount'))['amount__sum']
                booking.address = UserDetail.objects.get(user_id = booking.user.id).address
                booking.alter = UserDetail.objects.get(user_id = booking.user.id).alternate_no
        elif select == 'payment_type':
            bookings = Bookings.objects.filter()
            for booking in bookings:
                payment = PaymentDetails.objects.filter(booking_id = booking.id)
                for pay in payment:
                    booking.paymentname = pay.paymentname
                    if data == 'FirstInstallment Half'or 'FirstInstallment':
                        booking = PaymentDetails.objects.filter(paymentname = data) 
                        print(booking)
        else:
            booking = Bookings.objects.all()
            print(1821764)
            for booking in bookings:
                payments = booking.paymentdetails_set.all()
                booking.total_amt = payments.aggregate(Sum('amount'))['amount__sum']
                booking.address = UserDetail.objects.get(user_id = booking.user.id).address
                booking.alter = UserDetail.objects.get(user_id = booking.user.id).alternate_no
        context={
        'view_report': view_report,
        'project':project,
        'bookings':bookings,
        }
        return render(request, 'booking_report.html', context)
    content={
        'project':project,
        'bookings':bookings
        
    }
    return render(request, 'booking_report.html',content)

                        #site visit report

def site_report(request):
    sitereport_all = Site_visit.objects.all()
    print("Hello")
    if request.method == 'POST':
        value = request.POST.get('sitereportoption')
        select = request.POST.get('reportType')
        fromDate = request.POST.get('fromDate','')
        print('select:',select)
        print('value:',value)
        if select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                sitereport = Site_visit.objects.filter(created_on__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   created_on__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
                    
        elif select == 'project_head':
            sitereport = Site_visit.objects.filter(proj_head = value)
           
        elif select == 'executive':
            sitereport = Site_visit.objects.filter(executive = value)
            
        elif select == 'svstatus':
            sitereport = Site_visit.objects.filter(status = value)
            
        elif select == 'sourcewise':
            sitereport = Site_visit.objects.filter(source = value)
            
        elif select == 'svcategorywise':
            sitereport = Site_visit.objects.filter(sv_category = value)
        
        context={
        'sitereport_filter':sitereport,
        'sitereport': sitereport_all
        }
        return render(request, 'site_report.html', context)
    content={
        'sitereport_filter':sitereport_all,
        'sitereport': sitereport_all
        
    }
    return render(request, 'site_report.html', content)

