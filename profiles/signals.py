from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile,Relationship

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save,sender=Relationship)
def profile_relationship_friends(sender,instance,created,**kwargs):
	_send=instance.sender
	_receive=instance.receiver
	if instance.status=="accepted":
		_send.friends.add(_receive.user)
		_receive.friends.add(_send.user)
		_send.save()
		_receive.save()
		
@receiver(pre_delete,sender=Relationship)
def remove_from_friends(sender,instance,**kwargs):
	_send=instance.sender
	_receive=instance.receiver
	_send.friends.remove(_receive.user)
	_receive.friends.remove(_send.user)
	_send.save()
	_receive.save()