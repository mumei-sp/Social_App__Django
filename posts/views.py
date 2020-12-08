from django.shortcuts import render,redirect
from .models import Post,Like
from profiles.models import Profile
from .forms import PostCreateUpdateForm, CommentForm
from django.views.generic import DeleteView,UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def post_comment_list_view(request):
	qs = Post.objects.all()
	profile=Profile.objects.get(user=request.user)
	p_form=PostCreateUpdateForm()
	c_form=CommentForm
	if "post" in request.POST:
		p_form=PostCreateUpdateForm(request.POST)
		if p_form.is_valid():
			instance=p_form.save(commit=False)
			instance.author=profile
			instance.save()
			p_form=PostCreateUpdateForm()
	if "comment" in request.POST:
		c_form=CommentForm(request.POST)
		if c_form.is_valid():
			instance=c_form.save(commit=False)
			pk=request.POST.get("post_id")
			instance.post=Post.objects.get(id=pk)
			instance.user=profile
			instance.save()
			c_form=CommentForm()
	likes=Post.likes
	context = {
		'qs': qs,
		"profile":profile,
		"p_form":p_form,
		"c_form":c_form,
		"likes":likes,
		}
	return render(request, 'posts/all_posts.html', context)


class PostDeleteView(LoginRequiredMixin,DeleteView):
	model = Post
	template_name = 'posts/confirm_delete.html'
	success_url = reverse_lazy('posts')

	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		obj = Post.objects.get(pk=pk)
		if not obj.author.user == self.request.user:
			messages.warning(self.request, 'You need to be the author of the post in order to delete it')
		return obj

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		profile=Profile.objects.get(user=self.request.user)
		context["profile"]=profile
		return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
	form_class=PostCreateUpdateForm
	model=Post
	template_name="posts/update_post.html"
	success_url=reverse_lazy("posts")

	def form_valid(self,form,**kwargs):
		pk = self.kwargs.get('pk')
		post=Post.objects.get(id=pk)
		# or profile=Profile.objects.get(user=self.request.user)
			# if form.instance.author==profile
		if post.author.user == self.request.user:
			return super().form_valid(form)
		else:
			form.add_error(None, "You need to be the author of the post in order to update it")
			return super().form_invalid(form)


def like_unlike_post(request):
	pk=request.POST.get("post_id")
	profile=Profile.objects.get(user=request.user)
	post=Post.objects.get(id=pk)
	if request.method=="POST":
		liked,created=Like.objects.get_or_create(user=profile,post=post)
		if created:
			liked.value="like"
		else:
			if liked.value == "like":
				liked.value="unlike"
			else:
				liked.value="like"
		liked.save()
	return redirect("posts")
	
