from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,AbstractBaseUser,PermissionsMixin
)

class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None):
        if not email:
            raise ValueError('Enter Email!')
        user = self.model(
            username=username,
            email = email,
        )
        user.set_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None):
        user = self.model(
            username=username,
            email = email,
        )
        user.set_password(password)
        user.is_staff=True
        user.is_active=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    LANG_TYPES = (
        ('man', '男性'),
        ('woman', '女性'),
        ('no_answer', '無回答'),
    )
    user_id =models.AutoField(primary_key=True)
    username=models.CharField(max_length=30)
    email = models.EmailField(max_length=255,unique=True)
    gender=models.CharField(max_length=50,choices=LANG_TYPES,default='no_answer')
    comment=models.TextField(max_length=1000,blank=True,null=True)
    picture=models.ImageField(upload_to='user_picture/',blank=True,null=True,default='user_picture/noname_user.png')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False) 
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username'] 
    
    objects=UserManager()
    
    class Meta:
        verbose_name='ユーザ'
        verbose_name_plural='ユーザ一覧'
    
    def __str__(self):
        return self.username+':'+self.email
    
class Addresses(models.Model):
    CITY_NAMES=(
        ('池田市','池田市'),
        ('泉大津市','泉大津市'),
        ('泉佐野市','泉佐野市'),
        ('和泉市','和泉市'),
        ('茨木市','茨木市'),
        ('大阪狭山市','大阪狭山市'),
        ('大阪市','大阪市'),
        ('貝塚市','貝塚市'),
        ('柏原市','柏原市'),
        ('交野市','交野市'),
        ('河南町','河南町'),
        ('河内長野市','河内長野市'),
        ('岸和田市','岸和田市'),
        ('熊取町','熊取町'),
        ('堺市','堺市'),
        ('四條畷市','四條畷市'),
        ('島本町','島本町'),
        ('吹田市','吹田市'),
        ('摂津市','摂津市'),
        ('泉南市','泉南市'),
        ('太子町','太子町'),
        ('大東市','大東市'),
        ('高石市','高石市'),
        ('高槻市','高槻市'),
        ('田尻町','田尻町'),
        ('忠岡町','忠岡町'),
        ('千早赤阪村','千早赤阪村'),
        ('豊中市','豊中市'),
        ('豊能町','豊能町'),
        ('富田林市','富田林市'),
        ('寝屋川市','寝屋川市'),
        ('能勢町','能勢町'),
        ('羽曳野市','羽曳野市'),
        ('阪南市','阪南市'),
        ('東大阪市','東大阪市'),
        ('枚方市','枚方市'),
        ('藤井寺市','藤井寺市'),
        ('松原市','松原市'),
        ('岬町','岬町'),
        ('箕面市','箕面市'),
        ('守口市','守口市'),
        ('八尾市','八尾市'),
    )
    
    address_id= models.AutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    prefecture = models.CharField(max_length = 10,default='大阪府')
    city = models.CharField(max_length=10,choices=CITY_NAMES)
    address = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '住所'
        verbose_name_plural='住所一覧'
        
    def __str__(self):
        return self.user.username+':'+self.city+self.address