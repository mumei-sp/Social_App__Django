from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid
from django.db.models import Q



class Profiles_CustomManager(models.Manager):
	def all_profiles(self,user):
		return Profile.objects.all().exclude(user=user)
	def profile_to_invite(self,sender):
		all_profiles=Profile.objects.all().exclude(user=sender)
		profile=Profile.objects.get(user=sender)
		qs=Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))
		accepted=set()
		for i in qs:
			if i.status=="accepted":
				accepted.add(i.sender)
				accepted.add(i.receiver)
		can_invite=[i for i in all_profiles if i not in accepted]
		return can_invite
	def requested_profiles(self,sender):
		rel=Relationship.objects.filter(Q(receiver=sender) & Q(status="sent"))
		qs=[i.sender for i in rel]
		return qs

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE) # whenever a user is created profile created auto
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	bio = models.TextField(default="no bio...", max_length=300)
	email = models.EmailField(max_length=200, blank=True)
	avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
	friends = models.ManyToManyField(User, blank=True, related_name='friends')
	slug = models.SlugField(unique=True, blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	objects=Profiles_CustomManager()

	def no_of_posts(self):
		return self.post_set.all().count()
	def likes_received(self):
		posts=self.post_set.all()
		l=0
		for i in posts:
			l+=i.likes()
		return l
	def get_frnds(self):
		return self.friends.all()
	
	def __str__(self):
		return f"{self.user.username}-{self.created.strftime('%d-%m-%Y')}"
	
	def save(self, *args, **kwargs):
		if self.first_name and self.last_name:
			i_slug=slugify(self.first_name+" "+self.user.username)
		else:
			i_slug=slugify(self.user.username)
		self.slug = i_slug
		super().save(*args, **kwargs)


class Relationship(models.Model):
	st=(("sent","Sent"),("accepted","accepted"),)
	sender=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
	receiver=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
	status=models.CharField(max_length=10,choices=st)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.sender}-{self.status}"