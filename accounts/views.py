from django.shortcuts import render,redirect
from django.views.generic.base import TemplateView,View
from django.views.generic.edit import FormView
from .forms import UserLoginForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import SignUpForm,activate_user
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm,UserAddressEditForm
from django.contrib import messages
from .models import Addresses
from django.views.generic.detail import DetailView


User = get_user_model()




class HomeView(LoginRequiredMixin,TemplateView):
    template_name='home.html'

    
class UserLoginView(FormView):
    template_name='user_login.html'
    form_class=UserLoginForm
    
    def post(self,request,*args,**kwargs):
        email=request.POST['email']
        password=request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None and user.is_active:
            login(request,user)
        return redirect('boards:top')
    
class UserLogoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('accounts:user_login')
    
#新規登録用
class SignUpView(CreateView):
    form_class=SignUpForm
    success_url=reverse_lazy('accounts:user_login')
    template_name='signup.html'
    
    
class ActivateView(TemplateView):
    template_name='activate.html'
    
    def get(self,request,uidb64,token,*args,**kwargs): #URLのuidb64とtokenを取得,それらをactivate_user関数に渡す
        result = activate_user(uidb64,token) #正しく行われればresultにはTrueがはいる
        return super().get(request,result=result,**kwargs) #ここでのgetはTemplateViewのget。コンテキストとしてresultをテンプレートに渡す
    
#パスワードリセット用
class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'mail_template/reset/subject.txt'
    email_template_name = 'mail_template/reset/message.txt'
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'password_reset_confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'password_reset_complete.html'
    
    
#マイページ
class MypageView(TemplateView):
    template_name='mypage.html'
    
    def get(self,request,**kwargs):
        context={
            'user':self.request.user
        }
        return self.render_to_response(context)
    
#ユーザ情報更新する
@login_required
def user_edit(request):
    user_edit_form=UserEditForm(request.POST or None,request.FILES or None,instance=request.user)
    
    #Addressesが新規作成なのか更新なのかで分岐させる
    try:
        addresses=request.user.addresses
    except Addresses.DoesNotExist:
        addresses = None
    if addresses: #Addressesが存在すれば取得してフォームにいれる
        user_address_edit_form=UserAddressEditForm(request.POST or None,instance=addresses) #instanceにログインしているユーザのaddressesを指定
    else: #AddressesがなければAddressesは取得しない
        user_address_edit_form=UserAddressEditForm(request.POST or None)

    if user_edit_form.is_valid() and user_address_edit_form.is_valid():
        user_edit_form.save()
        if addresses: #住所更新の場合
            user_address_edit_form.save()
        else: #住所新規作成の場合
            user_address_edit_form.save(commit=False).user=request.user #Addressesのuserにログインしているユーザをいれてから
            user_address_edit_form.save() #user,prefecture,city,addressが揃ったので保存できる

        return redirect('accounts:mypage')
    # else:
    #     messages.error(request,'更新に問題があります')
    return render(request,'user_edit.html',context={
        'user_edit_form':user_edit_form,
        'user_address_edit_form':user_address_edit_form
    })
    
#ユーザ詳細ページ
class UserDetailView(DetailView):
    model =User
    template_name = 'user_detail.html'
    



def notify(request):
    subject="メールお試し送信" #日本語名だとコンソール上でsubjectは文字化けしてしまう
    message="これはメール送信のお試し関数です"
    from_email="sample1@gmail.com"
    recipient_list=[
        'microck.ryo@gmail.com'
    ]#宛先のアドレス
    send_mail(subject,message,from_email,recipient_list)
    return render(request,'send_mail.html')