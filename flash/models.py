from django.db import models
from datetime import datetime

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.files.storage import FileSystemStorage
#ここでuser登録の処理を定義
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError('メールアドレスを入力してください')
        if not username:
            raise ValueError('名前を入力してください')
        
        #メールアドレスを標準化する
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        #ハッシュ化したパスワードを作って入れる
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, username, password):
        #is_staffの項目を変えてユーザー登録処理
        user = self.create_user(email,username,password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, default='@gmail.com')
    username = models.CharField(max_length=255,unique=True)
    date_joined = models.DateTimeField(default=datetime.now())
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #これを使ってuserのハンドリングができるようになるらしい
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password','email']
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.username
    
fs = FileSystemStorage(location='videos')
class Movie(models.Model):
    movie = models.FileField(upload_to='videos/',storage=fs)
    originally_movie = models.FileField(upload_to='originally/',storage=fs,default=None)
    created = models.DateTimeField(verbose_name="投稿日時", auto_now_add=True, null=False, blank=False)
    post_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,default=None)
    thumbnail  = models.ImageField(upload_to='images/',storage=fs,default=None)

    public = models.BooleanField(default=False)
    rio_recommendation = models.BooleanField(default=False)
    # upload_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)