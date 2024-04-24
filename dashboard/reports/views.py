from django.shortcuts import render,redirect,HttpResponse
from dashboard.members.models import Bookings,PaymentDetails,Site_visit
from dashboard.projects.models import Project
from dashboard.userinfo.models import UserDetail,Executive,User,SeniorTeamLead
from django.urls import reverse
from num2words import num2words
from django.db.models import Sum
from datetime import datetime, date, timedelta
from django import template
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# Create your views here.
def confirmletter_view(request,id):
    book=Bookings.objects.get(id=id)
    user = User.objects.get(id=book.user_id)
    userdetail = UserDetail.objects.get(user=book.user)
    payment = PaymentDetails.objects.filter(booking=book)
    project = Project.objects.filter(landdetails=book.land_details)
    
      

    for i in payment:
        bank=i.bank
        branch=i.branch
        amount=i.amount
        print(amount)




    cheque_no=''
    dd_no=''
    netbanking=''
    

    for payment in payment:
        if payment.payment_mode == 'Cheque':
            cheque_no = payment.cheque_no
        elif payment.payment_mode == 'DD':
            dd_no = payment.ddno
        elif payment.payment_mode == 'Net Banking':
            netbanking = payment.transaction
    
    print(cheque_no)
    print(dd_no)
    print(netbanking)
    

    # for i in payment:
    #     bank = i.bank
    #     return render(request ,'confirmletter_view.html',{'book1':bank})
    # print("Muthu")
    return render(request,'confirmletter_view.html',{'user':user,
                                                     'book':book,
                                                     'amount':amount,
                                                     'bank':bank  if 'bank' in locals() else None,
                                                     'branch':branch  if 'branch' in locals() else None,
                                                     'userdetail':userdetail,
                                                     'payment':payment,
                                                     'netbanking':netbanking,
                                                     'dd_no':dd_no,
                                                     'cheque_no':cheque_no,
                                                     'project':project})
 

def print_recepit(request, id):
    try:
        paymentInfos = PaymentDetails.objects.filter(receipt_no=id).first()
        data = PaymentDetails.objects.filter()
        
       
      
        check_payments = PaymentDetails.objects.filter(dateofreceipt=paymentInfos.dateofreceipt , booking_id=paymentInfos.booking_id)
        details = PaymentDetails.objects.filter(receipt_no = paymentInfos.receipt_no, booking_id=paymentInfos.booking_id)
       
        for i in check_payments:
            print(i)
            if i.paymentname == "DownPayment":
                Value = PaymentDetails.objects.filter(dateofreceipt=paymentInfos.dateofreceipt , booking_id=paymentInfos.booking_id)
            else:
                Value = PaymentDetails.objects.filter(receipt_no = paymentInfos.receipt_no, booking_id=paymentInfos.booking_id)


        user = Bookings.objects.filter(user_id=paymentInfos.booking.user_id).first()
        
        if not user:
            return HttpResponse("No booking found for receipt number: {}".format(id))

        userdetail = UserDetail.objects.get(user=user.user)
        payments = PaymentDetails.objects.filter(booking_id=user.id)
        payment_count = payments.values('receipt_no').distinct().count()
        print(payment_count)
        id=id
        for payment in payments:
 
            last_payment = payment.amount
        if last_payment:
            no = float(last_payment)
            receipt_no = num2words(no)
            print(receipt_no)
        get_last = PaymentDetails.objects.filter(booking_id=user.id).last()
        value = get_last.amount
        no = float(value) 
        amont = float(value)+2600  
        word1 = num2words(amont, lang='en_IN')
        word = word1.replace(',','')
        print(no)
        print(amont)
        id=id 
        round_off = ''
        downpayment = ''

        for i in Value:
            if i.paymentname == 'Membership':
                word2 = float(value) + 2600
                word2 = num2words(word2, lang='en_IN')
                round_off = word2.replace(',','')
            else:
               amont = float(value)
               downpayment = num2words(amont, lang='en_IN')
               downpayment = downpayment.replace(',','')

        print('round off:', round_off)
        print('downpayment:', downpayment)
        
        total_membership = 0
        total_downpayment = 0
        total_first_installment = 0
        total_second_installment = 0
        total_third_installment = 0  

        for payment in payments:
            amount = float(payment.amount)  # Convert amount to float
            if payment.paymentname == "Membership":
                total_membership += amount
            elif payment.paymentname == "DownPayment":
                total_downpayment += amount
            elif payment.paymentname == "FirstInstallment":
                total_first_installment += amount
            elif payment.paymentname == "SecondInstallment":
                total_second_installment += amount
            elif payment.paymentname == "ThirdInstallment":
                total_third_installment += amount

        total_all = (
            total_membership +
            total_downpayment +
            total_first_installment +
            total_second_installment +
            total_third_installment
        )
        
        context = {
            'id': id,
            'user': user,   
            'detail':details,
            'word':word,
            'round_off':round_off,
            'downpayment':downpayment,
            'Value':Value,
            'userdetail': userdetail,
            'payment': payments,
            'payment_count': payment_count,
            'total_membership': total_membership,
            'total_downpayment': total_downpayment,
            'total_first_installment': total_first_installment,
            'total_second_installment': total_second_installment,
            'total_third_installment': total_third_installment,
            'total_all': check_payments.aggregate(Sum('amount'))['amount__sum'],
            'check_payment': check_payments
        }
        return render(request, 'print_recepit.html', context)
    except Exception as e:
        return HttpResponse("An error occurred: {}".format(e))
    
register = template.Library()

@register.filter
def add_amount(value):
    return int(value) + 2600
def booking_report(request):

    view_report = PaymentDetails.objects.all()
    project = Project.objects.all()
    bookings =Bookings.objects.all().order_by('-created_on')
    team_lead = User.objects.filter( role = "Project_Lead")
    executivename = User.objects.filter( role = "Executive")     
    
    if request.method == 'POST':
        data = request.POST.get('paymenttype')
        value = request.POST.get('projectOption')
        select = request.POST.get('reportType')
        teamlead = request.POST.get('projectOption')
        executtype = request.POST.get('projectexecut')
        if select == 'project':
            if value == 'all':
                bookings = Bookings.objects.all()
                print("All", bookings)
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
            sites = Site_visit.objects.filter(proj_head_id=teamlead)
            bookings = Bookings.objects.filter(sitevist__id=1)

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
            executive_id = SeniorTeamLead.objects.all()
            print(booking)
            for i in executive_id:
                print("id",i.user)
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
    team_lead = User.objects.filter( role = "Project_Lead")
    executivename = User.objects.filter( role = "Executive")
    print(team_lead)
    if request.method == 'POST':
        value = request.POST.get('sitereportoption')
        select = request.POST.get('reportType')

        if select == 'all':
            sitereport = Site_visit.objects.all()
        elif select == 'date':
            fromDate = request.POST.get('fromDate', '')
            toDate = request.POST.get('toDate', '')
            if toDate and fromDate:
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                toDate = datetime.strptime(toDate, '%Y-%m-%d') + timedelta(days=1)
                sitereport = Site_visit.objects.filter(
                    date_of_site_visit__gte=fromDate,
                    date_of_site_visit__lte=toDate
                ).all()
        elif select == 'project_head':
            sitereport = Site_visit.objects.filter(proj_head=value)
        elif select == 'executive':
            sitereport = Site_visit.objects.filter(executive=value)
        elif select == 'svstatus':
            sitereport = Site_visit.objects.filter(sv_status=value)
        elif select == 'sourcewise':
            sitereport = Site_visit.objects.filter(source=value)
        elif select == 'svcategorywise':
            sitereport = Site_visit.objects.filter(sv_category = value)
        
        context={
        'sitereport_filter':sitereport,
        'sitereport': sitereport_all,
        'team_lead':team_lead,
        'executivename':executivename
        }
        return render(request, 'site_report.html', context)
    content={
        'sitereport_filter':sitereport_all,
        'sitereport': sitereport_all,
        'team_lead':team_lead,
        'executivename':executivename
        
    }
    return render(request, 'site_report.html', content)

def pdc_report(request):
    return render(request, 'pdc_report.html')

def ugdg_report(request):
    ugdgreport_all = Bookings.objects.all()
    
    team_lead = User.objects.filter( role = "Project_Lead")
    executivename = User.objects.filter( role = "Executive")
    if request.method == 'POST':
        value = request.POST.get('sitereportoption')
        select = request.POST.get('reportType')

        if select == 'all':
            ugdgreport = Bookings.objects.all()
            ugdgreport = SeniorTeamLead.objects.filter()

        elif select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                ugdgreport = Bookings.objects.filter(date_of_change__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   date_of_change__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
                    
        elif select == 'project_wise':
            ugdgreport = Bookings.objects.filter(land_details__project__projectname = value)
           
        elif select == 'project_head':
            ugdgreport = Bookings.objects.filter(sitevist__proj_head =value)
            
        elif select == 'executive_wise':
            ugdgreport = Bookings.objects.filter(sitevist__executive = value)
            print(ugdgreport)
        elif select == 'type_change':
            ugdgreport = Bookings.objects.filter(type_of_change = value)
            
        elif select == 'ugpayment_wise':
            ugdgreport = Bookings.objects.filter(sv_category = value)
         
            
        
        context={
        'ugdgreport_filter':ugdgreport,
        'ugdgreport': ugdgreport_all,
        'executivename':executivename,
        'team_lead':team_lead
        }
        return render(request, 'ugdg_report.html', context)
    content={
        'ugdgreport_filter':ugdgreport_all,
        'ugdgreport': ugdgreport_all,
        'executivename':executivename,
        'team_lead':team_lead
        
    }
    return render(request, 'ugdg_report.html', content)

def transfer_report(request):
    transreport_all = Bookings.objects.all().order_by('-date_of_transfer')
    project = Project.objects.all()
    team_lead = User.objects.filter( role = "Project_Lead")

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
                    
        elif select == 'all':
            transreport = Bookings.objects.all()
            
        elif select == 'project_wise':
            transreport = Bookings.objects.filter(land_details__project__projectname = value)
           
        elif select == 'project_head':
            transreport = Bookings.objects.filter(sitevist__proj_head = value)
            
        context={
        'transreport_filter':transreport,
        'transreport': transreport_all,
        'project':project,
        'team_lead':team_lead,
        }
        return render(request, 'transfer_report.html', context)
    content={
        'transreport_filter':transreport_all,
        'transreport': transreport_all,
        'project':project,
        'team_lead':team_lead,
    }
    return render(request, 'transfer_report.html', content)

def cancel_report(request):
    cancelreport_all = Bookings.objects.all()
    team_lead = User.objects.filter( role = "Project_Lead")
    if request.method == 'POST':
        value = request.POST.get('cancelreportoption')
        select = request.POST.get('reportType')
        
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        if select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                cancelreport = Bookings.objects.filter(date_of_cancel__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   date_of_cancel__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
        elif select == 'refunddate':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                cancelreport = Bookings.objects.filter(date_of_refund__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   date_of_refund__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
        elif select == 'all':
            cancelreport = Bookings.objects.all() 
                 
        elif select == 'project_head':
            cancelreport = Bookings.objects.filter(sitevist__proj_head = value)
           
        elif select == 'mode_wise':
            cancelreport = Bookings.objects.filter(mode_of_refund = value)
            
        elif select == 'type_wise':
            cancelreport = Bookings.objects.filter(type_of_refund = value)

        context={
        'cancelreport_filter':cancelreport,
        'cancelreport': cancelreport_all,
        'team_lead':team_lead
        }
        return render(request, 'cancel_report.html', context)
    content={
        'cancelreport_filter':cancelreport_all,
        'cancelreport': cancelreport_all,
        'team_lead':team_lead
        
    }
    
    return render(request, 'cancel_report.html',content)

def receipt_details(request):
    receipts_all = PaymentDetails.objects.all().exclude(paymentname="Membership").order_by('-dateofreceipt')
    project = Project.objects.all()
    
        
    team_lead = User.objects.filter( role = "Project_Lead")
    if request.method == 'POST':
        value = request.POST.get('receiptreportoption')
        select = request.POST.get('reportType')
        
        fromDate = request.POST.get('fromDate','')
        toDate = request.POST.get('toDate','')
        if select == 'date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                receiptreport = PaymentDetails.objects.filter(dateofreceipt__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   dateofreceipt__lte=date(date_obj.year, date_obj.month, date_obj.day)).exclude(paymentname="Membership").all()
        elif select == 'c_date':
            fromDate = request.POST.get('fromDate','')
            toDate = request.POST.get('toDate','')
            if toDate and fromDate:
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                fromDate = datetime.strptime(fromDate, '%Y-%m-%d')
                date_obj = datetime.strptime(toDate, '%Y-%m-%d')
                toDate =  date_obj + timedelta(days=1)
                receiptreport = PaymentDetails.objects.filter(date_cleared__gte=date(fromDate.year, fromDate.month, fromDate.day),
                                                   date_cleared__lte=date(date_obj.year, date_obj.month, date_obj.day)).all()
        elif select == 'all':
            receiptreport = PaymentDetails.objects.all() 
            
        elif select == 'project_head':
            receiptreport = Bookings.objects.filter(sitevist__proj_head = value)
            print("Receipt Report:", receiptreport)
           
        elif select == 'mod_pay':
            receiptreport = PaymentDetails.objects.filter(payment_mode = value)
            
        elif select == 'pay_status':
            receiptreport = PaymentDetails.objects.filter(status = value)
            for i in receiptreport:
                print("Muthu",)
        elif select == 'customername':
            receiptreport = Site_visit.objects.filter(cust_name = value)
        elif select == 'project_wise':
            receiptreport = Bookings.objects.filter(land_details__project__projectname = value)
       
                             
        
        
        context={
        'receiptreport_filter':receiptreport,
        'receiptreport': receipts_all,
        'receipts_all': project,
        'team_lead':team_lead,
        }
        return render(request, 'receipt_details.html', context)
    content={
        'receiptreport_filter':receipts_all,
        'receiptreport': receipts_all,
        'receipts_all': project,
        'team_lead':team_lead,
       
        
    }
    
    return render(request, 'receipt_details.html',content)