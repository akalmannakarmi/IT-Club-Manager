from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpRequest
from django.shortcuts import render,get_object_or_404,redirect
from .models import Profile
from .forms import ProfileForm


def viewProfile(request:HttpRequest,profileId):
	profile = get_object_or_404(Profile, id=profileId)
	return render(request,"profiles/viewProfile.html",{"profile":profile})


@login_required
def viewMyProfile(request:HttpRequest):
	profile = get_object_or_404(Profile, id=request.user.id)
	return render(request,"profiles/viewMyProfile.html",{"profile":profile})


@login_required
def saveProfile(request:HttpRequest):
	if request.method == 'POST':
		profile = get_object_or_404(Profile, id=request.user.id)
		form = ProfileForm(request.POST,instance=profile)

		if form.is_valid():
			form.save()

		return redirect("/profile")
	return HttpResponse("Unsupported Method")
		