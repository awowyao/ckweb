from django.db import models

# Create your models here.


class Userinfo(models.Model):
    USER_TYPE = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )
    user_type = models.IntegerField(choices=USER_TYPE, blank=True, null=True)
    userName = models.CharField(max_length=10)
    userPwd = models.CharField(max_length=100)
    userTelphone = models.CharField(max_length=10)
    userAddress = models.CharField(max_length=10)
    userAge = models.CharField(max_length=4)
    userImg = models.CharField(max_length=200)


class UserToken(models.Model):
    user = models.OneToOneField(Userinfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    time = models.DateTimeField('创建时间', auto_now_add=True, null=True)

class usersImg(models.Model):
    userImg = models.ImageField(upload_to='static/user', null=True)

class Img_notice(models.Model):
    Img = models.TextField(null=True)
    title = models.TextField(null=True)
    topUrlimg = models.TextField(null=True)
    content = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class video_notice(models.Model):
    video = models.TextField(null=True)
    title = models.TextField(null=True)
    topUrlimg = models.TextField(null=True)
    content = models.TextField(null=True)
    time = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class user_visit(models.Model):
    ip = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now=True)