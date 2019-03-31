from django.db import models
from django.contrib.auth.models import User
from PIL import Image


# create name and path for every user
def user_directory_path(instance, filename):
    return f'id_images/user_id_{instance.user.id}/{filename}'

# create name and path for every profile
def profile_directory_path(instance, filename):
    return f'profile_pics/user_id_{instance.user.id}/{filename}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Profile Photo",
         default="default.jpg", upload_to=profile_directory_path)
    id_image = models.FileField(verbose_name="ID Photo",
        blank=True, default="default.jpg", upload_to=user_directory_path)
    trusted = models.BooleanField(default=False)
    id_number = models.CharField(verbose_name="ID Number",
        blank=True, max_length=20, null=True, unique=True)
    phone_number = models.CharField(verbose_name="Mobile Number",
        max_length=20, null=True, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    # resize profile images before saving to database
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 250 or img.width > 250:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)
