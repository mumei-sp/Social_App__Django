from django import forms
from .models import Post,Comment

class PostCreateUpdateForm(forms.ModelForm):
	class Meta:
		model=Post
		fields=["content","image"]

		widgets={
			"content": forms.Textarea(attrs={'class': "form-control","rows":"3","placeholder":"Add ur post.."}), 
			"image": forms.FileInput(attrs={'class': "custom-file"}),
			}

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields=["body"]
		widgets={
			"body": forms.Textarea(attrs={'class': "form-control","rows":"1","placeholder":"Add ur comment.."}), 
			}
