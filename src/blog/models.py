from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(draft=False).filter(published_date__lte=timezone.now())

class Post(models.Model):
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length=200)
	slug = models.SlugField(unique=True)
	text = models.TextField()
	created_date = models.DateTimeField(
			default=timezone.now)
	published_date = models.DateTimeField(
			blank=True, null=True)

	def publish(self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("blog:post", kwargs={"slug": self.slug})

	class Meta:
	    ordering = ["-created_date"] 

# if the title of the post occurs in multiple rows of the DB, the first 
# occurrence will just have the title slugified. The second occurrence will 
# have "-1" attached, etc. The counter is used to keep track and is 
# initialized with 1 in pre_save_blogpost_receiver.
def create_slug(instance, counter, new_slug=None):
    existing_slug = slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    queryset = Post.objects.filter(slug=slug).order_by("-id")
    exists = queryset.exists()
    if exists:
        new_slug = "%s-%s" %(existing_slug, counter)
        return create_slug(instance, counter + 1, new_slug=new_slug)
    return slug

# anytime a blog post is about to be saved this method checks for duplicates
def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance, 1)
        

pre_save.connect(pre_save_post_receiver, sender=Post)