from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField()
    image = models.ImageField(upload_to='images/%Y/%m/%d')
    description = models.TextField(blank=True)
    created = models.DateField(auto_now_add=True,
                               db_index=True)
    # 我们需要一个多对多关系。因为一个用户可能喜欢很多张图片，一张图片也可能被很多用户喜欢
    user_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='images_liked',
                                       blank=True)

    # 自动生成slug
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
