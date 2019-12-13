import requests
from cStringIO import StringIO

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models, transaction

from django_images.models import Image as BaseImage, Thumbnail
# from taggit.managers import TaggableManager

# from ..users.models import User
from django.contrib.auth.models import User
from vote.models import VoteModel


class ImageManager(models.Manager):
    # FIXME: Move this into an asynchronous task
    def create_for_url(self, url):
        file_name = url.split("/")[-1].split('#')[0].split('?')[0]
        buf = StringIO()
        response = requests.get(url)
        buf.write(response.content)
        obj = InMemoryUploadedFile(buf, 'image', file_name,
                                   None, buf.tell(), None)
        # create the image and its thumbnails in one transaction, removing
        # a chance of getting Database into a inconsistent state when we
        # try to create thumbnails one by one later
        image = self.create(image=obj)
        for size in settings.IMAGE_SIZES.keys():
            Thumbnail.objects.get_or_create_at_size(image.pk, size)
        return image


class Image(BaseImage):
    objects = ImageManager()

    class Meta:
        proxy = True


class Pin(VoteModel,models.Model):
    submitter = models.ForeignKey(User)
    url = models.URLField(null=True)
    origin = models.URLField(null=True)
    price = models.FloatField(null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ForeignKey(Image, related_name='pin')
    published = models.DateTimeField(auto_now_add=True)
    # tags = TaggableManager()
    like_count = models.IntegerField(null= False, default= 0 )
    tao_kouling = models.CharField(max_length=100,blank=True, null=True)
    num_iid = models.IntegerField(null=True,unique=True)
    #expire_date = models.DateTimeField()

    def __unicode__(self):
        return '%s - %s' % (self.submitter, self.published)


class ExpiredPin(models.Model):
    num_iid = models.IntegerField(null=True)
    def __unicode__(self):
        return '%s' % (self.num_iid)


class Activation(models.Model):
    activate_code = models.CharField(null=True,max_length=100)
    uid = models.CharField(null=True,max_length=100,blank=True)
    times = models.IntegerField(null=True,default = 0)
    expired_date = models.DateField(blank=True, null=True)
    owner = models.ForeignKey(User,blank=True,null=True)
    used = models.BooleanField(default = False)
    value = models.IntegerField(null=True,default = 1)

class Order(models.Model):
    uid = models.CharField(null=True,max_length=100,blank=True)
    customer = models.ForeignKey(User)
    created_time = models.DateField(auto_now=True)
    amount = models.IntegerField()
    order_status = models.BooleanField()


    # def __unicode__(self):
    #     return '%s - %s' % (self.customer, self.uid)

class Token(models.Model):
    token = models.CharField(null=True,max_length=100,blank=True)
