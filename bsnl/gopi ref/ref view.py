from django.shortcuts import render, redirect
from .models import Login 

def create(request):
    if request.method == 'POST':
        Login(
            name=request.POST['namedb'],
            email=request.POST['emaildb'],
            password=request.POST['passworddb'],

        ).save()
    return render(request, 'index.html')

def view(request):
    name=Login.objects.all()
    return render(request,'view.html',{'name':name})

def update(request,id):
    updname=Login.objects.get(id=id)
    if request.method == "POST":
        updname.name = request.POST['namedb']
        updname.email = request.POST['emaildb']
        updname.password = request.POST['passworddb']
        updname.save()
    return render(request,'update.html',{'upname':updname}) 

def delete(request, id):
    ddelete = Login.objects.get(id=id)
    ddelete.delete()
    return redirect(view)