from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Entry(models.Model):
    """Model definition for Entry."""

    # TODO: Define fields here
    name = models.CharField(max_length = 20,blank=True, null=True)
    url = models.CharField(max_length=100,blank=True, null=True)
    zipkey = models.CharField(max_length=50, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        """Meta definition for Entry."""

        verbose_name = 'Entry'
        verbose_name_plural = 'Entrys'

    def __str__(self):
        """Unicode representation of Entry."""
        return self.name

# class Ownership(models.Model):
#     """Model definition for Ownership."""
    
#     name = models.ForeignKey('User', related_name='', on_delete=models.CASCADE)
#     # TODO: Define fields here

#     class Meta:
#         """Meta definition for Ownership."""

#         verbose_name = 'Ownership'
#         verbose_name_plural = 'Ownerships'

#     def __str__(self):
#         """Unicode representation of Ownership."""
#         pass


    # TODO: Define custom methods here

