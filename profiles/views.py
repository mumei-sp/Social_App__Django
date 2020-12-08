from django.shortcuts import render,redirect,get_object_or_404
from .models import Profile,Relationship
from .forms import ProfileUpdateForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def profile_view(request):
	ps=Profile.objects.get(user=request.user)
	form=ProfileUpdateForm(instance=ps)
	if request.method=="POST":
		form=ProfileUpdateForm(request.POST, request.FILES or None, instance=ps)
		if form.is_valid():
			form.save()
	frnds_exists=True
	if ps.friends.all().count()==0 :
		frnds_exists=False
	context={"profile":ps,"form":form,"frnds_exists":frnds_exists,}
	return render(request,"profiles/profile.html",context)

class Profiles_ListView(LoginRequiredMixin,ListView):
	model=Profile
	template_name="profiles/all_profiles.html"
	context_object_name="qs"

	def get_queryset(self):
		qs=Profile.objects.all_profiles(self.request.user)
		return qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(username__iexact=self.request.user)
		profile = Profile.objects.get(user=user)
		rel_r = Relationship.objects.filter(sender=profile)
		rel_s = Relationship.objects.filter(receiver=profile)
		rel_receiver = []
		rel_sender = []
		for item in rel_r:
			rel_receiver.append(item.receiver.user)
		for item in rel_s:
			rel_sender.append(item.sender.user)
		context["rel_receiver"] = rel_receiver
		context["rel_sender"] = rel_sender
		context['is_empty'] = True if len(self.get_queryset()) == 0 else False
		return context

@login_required
def invite_profiles_ListView(request):
	profile=Profile.objects.get(user=request.user)
	qs = Profile.objects.profile_to_invite(request.user)
	rel_s=Relationship.objects.filter(Q(sender=profile) & Q(status="sent"))
	rel_r=Relationship.objects.filter(Q(receiver=profile) & Q(status="sent"))
	rel=[i.sender.user for i in rel_r]
	rel.extend([i.receiver.user for i in rel_s])

	is_empty=False
	if len(qs) == 0:
		is_empty=True
	context = {'qs': qs,"is_empty":is_empty,"rel":rel,}
	return render(request, 'profiles/can_invite.html', context)
@login_required
def received_invites(request):
	profile=Profile.objects.get(user=request.user)
	qs=Profile.objects.requested_profiles(profile)
	is_empty=False
	if len(qs)==0: is_empty=True
	return render(request,"profiles/invites_received.html",{"qs":qs,"is_empty":is_empty})
@login_required
def send_invitation(request):
	if request.method=="POST":
		sender=Profile.objects.get(user=request.user)
		pk=request.POST.get("profile_pk")
		receiver=Profile.objects.get(id=pk)
		Relationship.objects.create(sender=sender,receiver=receiver,status="sent")
		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('all_profiles')
@login_required
def remove_friends(request):
	if request.method=="POST":
		my_profile=Profile.objects.get(user=request.user)
		pk=request.POST.get("profile_pk")
		frnd_profile=Profile.objects.get(id=pk)
		rel=Relationship.objects.filter(Q(sender=my_profile) & Q(receiver=frnd_profile) | Q(sender=frnd_profile) & Q(receiver=my_profile))
		rel.delete()
		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('all_profiles')
@login_required
def reject_request(request):
	if request.method=="POST":
		profile=Profile.objects.get(user=request.user)
		pk=request.POST.get("profile_pk")
		send_profile=Profile.objects.get(id=pk)
		rel=Relationship.objects.get(Q(sender=send_profile) & Q(receiver=profile))
		rel.delete()
		return redirect(request.META.get('HTTP_REFERER'))
	return redirect('received_invites')
@login_required
def accept_request(request):
	if request.method=="POST":
		receiver=Profile.objects.get(user=request.user)
		pk=request.POST.get("profile_pk")
		sender=Profile.objects.get(id=pk)
		rel=get_object_or_404(Relationship,sender=sender,receiver=receiver)
		if rel.status=="sent":
			rel.status="accepted"
			rel.save()
	return redirect('received_invites')

class Profile_DetailView(LoginRequiredMixin,DetailView):
	model=Profile
	template_name="profiles/detail_profile.html"

	def get_context_data(self,**kwargs):
		context = super().get_context_data(**kwargs)
		user = User.objects.get(username__iexact=self.request.user)
		profile = Profile.objects.get(user=user)
		rel_r = Relationship.objects.filter(sender=profile)
		rel_s = Relationship.objects.filter(receiver=profile)
		rel_receiver = []
		rel_sender = []
		for item in rel_r:
			rel_receiver.append(item.receiver.user)
		for item in rel_s:
			rel_sender.append(item.sender.user)
		context["rel_receiver"] = rel_receiver
		context["rel_sender"] = rel_sender
		#context['is_empty'] = True if len(self.get_queryset()) == 0 else False
		return context