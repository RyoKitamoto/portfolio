from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.conf import settings
#トークン生成用
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import send_mail
from .models import Addresses


User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password= forms.CharField(label='パスワード',widget=forms.PasswordInput)
    
#新規登録用
subject="仮登録メール"
message_template="""
仮登録ありがとうございます。
以下URLをクリックして登録を完了してください。

"""
    #URLを生成する関数
def get_activate_url(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return settings.FRONTEND_URL + "accounts/activate/{}/{}".format(uid,token)

class SignUpForm(UserCreationForm):
    username=forms.CharField(label='ニックネーム')
    email=forms.EmailField(label='メールアドレス')
    
    class Meta:
        model = User
        fields=('username','email','password1','password2')
        
    def save(self,commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        #POSTされたらget_activate_url関数で作られたURLをメッセージにくっつけて送信
        if commit:
            user.save()
            activate_url = get_activate_url(user)
            message = message_template + activate_url
            from_email=settings.DEFAULT_FROM_EMAIL
            # user.email_user(subject,message)
            send_mail(subject,message,from_email,[user.email])
            
        return user

#ユーザを有効化する関数
def activate_user(uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode() #uidを復元
        user = User.objects.get(pk=uid) #userを見つける
    except Exception:
        return False
    
    #tokenのチェックもOKならis_activeをTrueにする
    if default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        return True
    
    return False

#ユーザ情報を更新するフォーム
class UserEditForm(forms.ModelForm):
    LANG_TYPES = (
        ('man', '男性'),
        ('woman', '女性'),
        ('no_answer', '無回答'),
    )
    username=forms.CharField(label='ニックネーム',max_length=30)
    gender=forms.ChoiceField(label='性別',choices=LANG_TYPES)
    comment=forms.CharField(label='コメント',required=False,widget=forms.Textarea(attrs={
        'placeholder':'取引しやすくなるように自己紹介文を書こう'
    }))
    picture=forms.FileField(label='プロフィール画像',required=False,widget=forms.FileInput(attrs={'class':'custom-file-input'}),)

    class Meta:
        model =User
        fields=('username','gender','comment','picture')
        
#住所更新フォーム
class UserAddressEditForm(forms.ModelForm):
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
    prefecture = forms.CharField(label='都道府県',max_length=10,disabled=True,initial='大阪府')
    city= forms.ChoiceField(label='市町村',choices=CITY_NAMES)
    address = forms.CharField(label='その他住所',max_length=30)
    
    class Meta:
        model=Addresses
        fields=('prefecture','city','address')