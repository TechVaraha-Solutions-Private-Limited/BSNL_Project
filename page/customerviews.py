from django.shortcuts import render,get_object_or_404,HttpResponse,redirect
# from app.models import Project,Receipt,User,Role
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
# from app.models import Newbooking
from django.http import FileResponse
from django.views.generic import View
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
@login_required
def home(request):
    return render(request,'page/customer/home.html')

@login_required
# def product(request):
#     user = request.user
#     rec = Receipt.objects.filter(username=user.username)
#     for r in rec:
#         print(r.username)
#     return render(request,'page/customer/product.html',{'user':user})

@login_required
def payment(request):
    return render(request,'page/customer/payment.html')

@login_required
def pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf,pagesize=letter)
    textob =c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica",14)

    lines =[
        'this qmmmmm'
    ]
    for line in lines:
        textob.textLine(line)
        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True,filename='text.pdf')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')