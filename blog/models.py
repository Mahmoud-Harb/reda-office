from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# create name and path for every user
def user_directory_path(instance, filename):
    return f'files/user_id_{instance.author.id}_{instance.author.username}/{filename}'

class Post(models.Model):
    title = models.CharField(verbose_name="العنوان" ,max_length=100)
    content = models.TextField(verbose_name="المحتوى" ,blank=True)
    file_upload = models.FileField(verbose_name="ارفع ملف",
        blank=True, default=None, upload_to=user_directory_path)
    image_upload = models.ImageField(verbose_name="ارفع صورة",
        blank=True, upload_to=user_directory_path)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.pk})


class Reply(models.Model):
    reply = models.TextField(verbose_name="اضف رد")
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.reply
