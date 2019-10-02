from django.db import models
from django.contrib.auth.models import User
from PIL import Image

from phone_field import PhoneField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = PhoneField(blank=True, help_text='Contact phone number')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self,*args,**kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            #img.save(self.Image_path))


class SharedMessage(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    receiver = models.ForeignKey(User,on_delete= models.CASCADE,related_name="receiver")
    file_location = models.FilePathField(default="",max_length=300)
    link = models.TextField(default='')
    note = models.TextField(default='')
    local_time = models.DateTimeField()
    ust_time = models.DateTimeField()
    exp_time = models.IntegerField()

    def __str__(self):
        return str(self.pk)