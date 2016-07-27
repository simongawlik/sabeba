from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import PostForm
from .models import Post

# Create your views here.
def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	query = request.GET.get("q")
	if query:
		posts = posts.filter(
			Q(title__icontains=query) |
			Q(body__icontains=query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
			).distinct()
	paginator = Paginator(posts, 4) # Show 4 blog entries per page
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)
	return render(request, 'post_list.html', {'posts': queryset, 'page_request_var': page_request_var})

def post_detail(request, slug):
	post = get_object_or_404(Post, slug=slug)
	return render(request, 'post_detail.html', {'post': post})

@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.save()
			return redirect('post_detail', slug=post.slug)
	else:
		form = PostForm()
	return render(request, 'post_edit.html', {'form': form})


@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
    	form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
	return render(request, 'post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, slug):
	post = get_object_or_404(Post, slug=slug)
	post.publish()
	return redirect('blog.views.post_detail', slug=slug)

@login_required
def post_remove(request, slug):
	post = get_object_or_404(Post, slug=slug)
	post.delete()
	return redirect('blog.views.post_list')