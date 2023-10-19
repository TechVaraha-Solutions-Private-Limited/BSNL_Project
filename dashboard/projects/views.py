from django.shortcuts import render,redirect
from dashboard.projects.models import Project,PlotSize,LandDetails
from django.contrib import messages

def addproject(request):
	if request.method == 'POST':
		Project(
            projectname = request.POST['projectname'].upper(),
	        shortcode = request.POST['shortcode'].upper(),
	        state = request.POST['state'],
			city = request.POST['city'],
			pincode = request.POST['pincode'],
	        images = request.FILES['imageupload'],
	        address = request.POST['address'],
			gmap = request.POST['gmaplink'],
	        updated_by = request.user
            ).save()
		messages.error(request,'Successfully Saved')
	return render(request, 'add_project.html')
    

def addplotsize(request):
	if request.method == 'POST':
		PlotSize(
			plotsize = request.POST['plotsize']+'X'+request.POST['plotsize1']
			).save()
		messages.error(request,'Successfully Saved')
	else:
		None
	data = PlotSize.objects.all()
	return render(request,'add_plot_size.html',{'data':data})
def updateplotsize(request,id):
	updateproject=PlotSize.objects.get(id=id)
	return render(request,'update_project_list.html',{'updateproject':updateproject})

def deleteplotsize(request,id):
	deletingprojectlist=PlotSize.objects.get(id=id)
	deletingprojectlist.delete()
	return redirect(addplotsize)

def addlandinfo(request):
    projects = Project.objects.all()
    pltsizes = PlotSize.objects.all()

    if request.method == 'POST':
        project_id = request.POST['projectname']
        plotsize_id = request.POST['plotsize']

        project_instance = Project.objects.get(id=project_id)
        plotsize_instance = PlotSize.objects.get(id=plotsize_id)
		
        LandDetails.objects.create(
            project=project_instance,
            plotsize=plotsize_instance,
            per_square_feet_amount=request.POST['persquarefeetamount'],
            total_amount=request.POST['totalamount'],
            down_payment=request.POST['downamount'],
            installment_1=request.POST['firstinstallment'],
            installment_2=request.POST['secondinstallment'],
            installment_3=request.POST['thirdinstallment'],
            updated_by=request.user
        )
			
        return redirect('addlandinfo')

    return render(request, 'add_land_info.html', {'projects': projects, 'pltsizes': pltsizes})

def projectlist(request):
	projectslists=Project.objects.all()
	return render(request,'project_list.html',{'projectslists':projectslists})

def updateprojectlist(request,id):
	updateproject=Project.objects.get(id=id)

	return render(request,'update_project_list.html',{'updateproject':updateproject})

def updatingprojectlist(request,id):
	updatingprojectlist=Project.objects.get(id=id)
	updatingprojectlist.projectname = request.POST['projectname'].upper()
	updatingprojectlist.shortcode = request.POST['shortcode'].upper()
	updatingprojectlist.address = request.POST['address']
	updatingprojectlist.state = request.POST['state']
	updatingprojectlist.city = request.POST['city']
	updatingprojectlist.pincode = request.POST['pincode']
	#updated_by = request.user
	updatingprojectlist.save()
	print(id)
	return redirect(projectlist)
	print(id)
def deleteprojectlist(request,id):
	deletingprojectlist=Project.objects.get(id=id)
	deletingprojectlist.delete()
	return redirect(projectlist)

def landrecords(request):
	landdetails=LandDetails.objects.all()
	return render(request,'land_records.html',{'landdetails':landdetails})

def updatelandrecords(request,id):
	updatelandrecords=LandDetails.objects.get(id=id)
	return render(request,'update_land_records.html',{'updatelandrecords':updatelandrecords})

def updatinglandrecords(request,id):
	updatinglandrecords=LandDetails.objects.get(id=id)
	updatinglandrecords.per_square_feet_amount=request.POST['persquarefeetamount']
	updatinglandrecords.total_amount=request.POST['totalamount']
	updatinglandrecords.down_payment=request.POST['downamount']
	updatinglandrecords.installment_1=request.POST['firstinstallment']
	updatinglandrecords.installment_2=request.POST['secondinstallment']
	updatinglandrecords.installment_3=request.POST['thirdinstallment']        
	#updated_by = request.user
	updatinglandrecords.save()
	return redirect(landrecords)

def deletelandrecords(request,id):
	deletinglandrecords=LandDetails.objects.get(id=id)
	deletinglandrecords.delete()
	return redirect(landrecords)