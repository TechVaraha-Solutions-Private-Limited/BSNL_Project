from django.shortcuts import render,redirect,HttpResponse
from dashboard.members.models import Bookings,PaymentDetails,Site_visit
from dashboard.projects.models import Project
from dashboard.userinfo.models import UserDetail,Executive,User
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
    team_lead = User.objects.filter( role = "Project_Lead")
    executivename = User.objects.filter( role = "Executive")     
    for view in view_report:
        detail = UserDetail.objects .get(user_id = view.booking.user)
        view.userinfo = detail.alternate_no
        view.address = detail.address

    if request.method == 'POST':
        data = request.POST.get('paymenttype')
        value = request.POST.get('projectOption')
        select = request.POST.get('reportType')
        teamlead = request.POST.get('projectOption')
        executtype = request.POST.get('projectexecut')
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
            #bookings = Bookings.objects.filter(sitevist__executive__executive_set__last__teamlead__sr_team__project_head__first_name= teamlead)
            
            bookings = Bookings.objects.filter(sitevist__executive__id__in=[6])

            for booking in bookings:
                print(booking)
        elif select == 'executive':
            bookings = Bookings.objects.filter(sitevist__executive = executtype)
        elif select == 'payment_type':
            if data == 'DownPayment':
                print('DownPayment',data)
                bookings = Bookings.objects.filter(payments_status__in=[1,4])
            elif data == 'FirstInstallment':
                bookings = Bookings.objects.filter(payments_status__in=[3,6])
                print('1st',data)
            elif data == 'SecondInstallment':
                print('2nd',data)
                bookings = Bookings.objects.filter(payments_status__in=[5,8])
            elif data == 'ThridInstallment':
                print('3rd',data)
                bookings = Bookings.objects.filter(payments_status__in=[7,9])
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
        'team_lead':team_lead,
        'executivename':executivename,
        }
        return render(request, 'booking_report.html', context)
    content={
        'project':project,
        'bookings':bookings,
        'team_lead':team_lead,
        'executivename':executivename
    }
    return render(request, 'booking_report.html',content)

                        #site visit report

def site_report(request):
    sitereport_all = Site_visit.objects.all()

    if request.method == 'POST':
        value = request.POST.get('sitereportoption')
        select = request.POST.get('reportType')

        if select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                sitereport = Site_visit.objects.filter(date_of_site_visit__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   date_of_site_visit__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
                    
        elif select == 'project_head':
            sitereport = Site_visit.objects.filter(proj_head = value)
           
        elif select == 'executive':
            sitereport = Site_visit.objects.filter(executive = value)
            
        elif select == 'svstatus':
            sitereport = Site_visit.objects.filter(sv_status = value)
            
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

def pdc_report(request):
    return render(request, 'pdc_report.html')

def ugdg_report(request):
    return render(request, 'ugdg_report.html')

def transfer_report(request):
    transreport_all = Bookings.objects.all()
    project = Project.objects.all()

    if request.method == 'POST':
        value = request.POST.get('sitereportoption')
        select = request.POST.get('reportType')
        fromDate = request.POST.get('fromDate','')

        if select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                transreport = Bookings.objects.filter(date_of_transfer__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   date_of_transfer__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
                    
        elif select == 'project_wise':
            transreport = Bookings.objects.filter(land_details__project__projectname = value)
           
        elif select == 'project_head':
            transreport = Bookings.objects.filter(project_wise = value)
            
        context={
        'transreport_filter':transreport,
        'transreport': transreport_all,
        'project':project,
        }
        return render(request, 'transfer_report.html', context)
    content={
        'transreport_filter':transreport_all,
        'transreport': transreport_all,
        'project':project,
        
    }
    return render(request, 'transfer_report.html', content)

def cancel_report(request):				
    return render(request, 'cancel_report.html')

def receipt_details(request):
    receipts_all = PaymentDetails.objects.all()
    
    if request.method == 'POST':
        value = request.POST.get('receiptreportoption')
        select = request.POST.get('reportType')
        fromDate = request.POST.get('fromDate','')
        if select == 'receipt_date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                receiptreport = PaymentDetails.objects.filter(dateofreceipt__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   dateofreceipt__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
                return receiptreport
        elif select == 'project_head':
            receiptreport = PaymentDetails.objects.filter(proj_head = value)
           
        elif select == 'mod_pay':
            receiptreport = PaymentDetails.objects.filter(payment_mode = value)
            
        elif select == 'pay_status':
            receiptreport = PaymentDetails.objects.filter(status = value)

        context={
        'receiptreport_filter':receiptreport,
        'receiptreport': receipts_all
        }
        return render(request, 'receipt_details.html', context)
    content={
        'receiptreport_filter':receipts_all,
        'receiptreport': receipts_all
        
    }
    
    return render(request, 'receipt_details.html',content)