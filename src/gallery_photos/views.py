from django.shortcuts import render

from .models import Photo

# Create your views here.
def home(request):
	queryset = Photo.objects.all()
	context = {
		"image_list": queryset,
		"title": "List"
	}
	return render(request, "gallery.html", context)
