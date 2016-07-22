from django.db import models

# Create your models here.
class Photo(models.Model):
	title = models.CharField(max_length=120, blank=True, null=True)
	image_path = models.ImageField(upload_to='photos/')
	timestamp_posted = models.DateTimeField(auto_now_add=True, auto_now=False)
	timestamp_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	alternative_text = models.CharField(max_length=120, blank=True, null=True)
	height = models.PositiveSmallIntegerField()
	width = models.PositiveSmallIntegerField()
	artist = models.CharField(default='Saba', max_length=120, blank=True, null=True)

	def __str__(self):
		return self.title