from django.shortcuts import render,redirect

# Create your views here.
def confirmletter_view(request):
    return render(request,'confirmletter_view.html')