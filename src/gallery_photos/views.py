from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Photo

# Create your views here.
def gallery(request):
	queryset_list = Photo.objects.all()
	paginator = Paginator(queryset_list, 4) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context = {
		"image_list": queryset,
		"title": "List"
	}
	return render(request, "gallery.html", context)

def image_detail(request, id):
	instance = get_object_or_404(Photo, id=id)
	context = {
		"title": instance.title,
		"instance": instance,
	}
	return render(request, "image_detail.html", context)


    