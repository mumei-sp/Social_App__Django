from django.urls import path
from .views import (profile_view, Profiles_ListView, 
				invite_profiles_ListView, received_invites, 
				send_invitation, remove_friends, reject_request, 
				accept_request, Profile_DetailView, )

urlpatterns=[
			path("",profile_view,name="profile"),
			path("all_profiles/",Profiles_ListView.as_view(),name="all_profiles"),
			path("to_invite/",invite_profiles_ListView,name="to_invite"),
			path("received_invites/",received_invites,name="received_invites"),
			path("send_invitation/",send_invitation,name="send_invitation"),
			path("remove_friends/",remove_friends,name="remove_friends"),
			path("accept_request/",accept_request,name="accept_request"),
			path("reject_request/",reject_request,name="reject_request"),
			path("<slug>/",Profile_DetailView.as_view(),name="detail_profile"),
			]