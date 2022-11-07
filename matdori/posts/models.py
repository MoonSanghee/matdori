from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=20)
    address = models.CharField(max_length=50)
    sectors = models.CharField(max_length=20)
    phonenumber = models.CharField(max_length=30, blank=True)
    characteristic = models.CharField(max_length=50, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=""
    )
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        format="JPEG",
    )

    thumbnail = ProcessedImageField(
        upload_to="images/",
        blank=True,
        processors=[ResizeToFill(400, 240)],
        format="JPEG",

        options={"quality": 100},
    )


    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")


class Review(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    grade = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=None
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = ProcessedImageField(
        upload_to="images/",
        blank=True,
        format="JPEG",
    )
    def summary(self):
        return self.content[:50]  