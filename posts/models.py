from django.db import models
from profiles.models import Profile
from django.core.validators import FileExtensionValidator

class Post(models.Model):
	author=models.ForeignKey(Profile,on_delete=models.CASCADE)
	content=models.TextField(max_length=200)
	#image=models.ImageField(upload_to='posts', validators=[FileExtensionValidator(['png', 'jpg', 'jpeg'])],blank=True)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	class Meta:
		ordering=["-created"]

	def __str__(self):
		return str(self.content)[:20]

	def likes(self):
		return self.like_set.filter(value="like").count()

class Comment(models.Model):
	body=models.TextField(max_length=100)
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	user=models.ForeignKey(Profile,on_delete=models.CASCADE)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.body


st=(("like","Like"),
	("unlike","Un-Like"),)

class Like(models.Model):
	post=models.ForeignKey(Post,on_delete=models.CASCADE)
	user=models.ForeignKey(Profile,on_delete=models.CASCADE)
	value=models.CharField(max_length=10,choices=st)
	updated = models.DateTimeField(auto_now=True)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f"{self.user}-{self.post}-{self.value}"

