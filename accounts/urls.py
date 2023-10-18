from django.urls import path
from .views import HomeView,UserLoginView,UserLogoutView,notify,SignUpView,ActivateView,PasswordReset,PasswordResetDone,PasswordResetConfirm,PasswordResetComplete,MypageView,user_edit,UserDetailView

app_name='accounts'

urlpatterns=[
    path('home/',HomeView.as_view(),name='home'),
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('logout/',UserLogoutView.as_view(),name='user_logout'),
    path('send_mail/',notify,name='send_mail'), #おためし
    path('signup/',SignUpView.as_view(),name='signup'),
    path('activate/<uidb64>/<token>',ActivateView.as_view(),name='activate'),
    path('password_reset/', PasswordReset.as_view(), name='password_reset'), 
    path('password_reset/done/', PasswordResetDone.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetComplete.as_view(), name='password_reset_complete'),
    path('mypage/', MypageView.as_view(), name='mypage'),
    path('user_edit/', user_edit, name='user_edit'),
    path('user_detail/<int:pk>/',UserDetailView.as_view() , name='user_detail'),
]