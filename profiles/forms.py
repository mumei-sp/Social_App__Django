from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model=Profile
		fields=["first_name","last_name","email","bio","avatar"]

		widgets={
			"first_name": forms.TextInput(attrs={'class': "form-control"}),
			"last_name": forms.TextInput(attrs={'class': "form-control"}),
			"email":forms.TextInput(attrs={"class":"form-control","place_holder":"x.x.x.x@gmail.com"}),
			"bio": forms.Textarea(attrs={'class': "form-control","rows":3,}), 
			"avatar": forms.FileInput(attrs={'class': "custom-file"}),
			}