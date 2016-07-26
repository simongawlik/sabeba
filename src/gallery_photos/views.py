from django.shortcuts import render, get_object_or_404

from .models import Photo

# Create your views here.
def gallery(request):
	queryset = Photo.objects.all()
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