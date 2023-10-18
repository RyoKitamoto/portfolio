from django.shortcuts import render,redirect,get_object_or_404
from .models import Items,ItemPictures
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import DeleteView,UpdateView,CreateView
from django.views.generic.base import TemplateView
from .forms import ItemCreateForm,ItemPicturesCreateForm,ItemEditForm,ItemPictureEditForm
from django.urls import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ContactForm
from .models import Contact,Items
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import ItemSearchForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from accounts.models import Addresses
from django.db.models import Count
from django.contrib.auth.mixins import LoginRequiredMixin



class TopView(ListView):
    model = Items
    template_name = 'top.html'
    paginate_by = 6
    
    
    def get_queryset(self):
        # ListViewのデフォルトのget_querysetを呼び出し、クエリセットを取得
        qs = super().get_queryset()
        self.form = form = ItemSearchForm(self.request.GET or None)

        if form.is_valid():
            search_query = form.cleaned_data['search']
            category_filter = form.cleaned_data['category']

            #フリーワードの空白を区切り、順番に絞るand検索
            if search_query:
                for word in search_query.split():
                    qs = Items.objects.search(query=word)
                    
            #カテゴリがあればさらに絞り込む
            if category_filter:
                qs = qs.filter(category=category_filter)
        qs = qs.order_by('-created_at')
        return qs
    
    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['form']=self.form
        #cityの件数を取得
        city_items_counts = Addresses.objects.values('city').annotate(item_count=Count('user__items')).order_by('city')
        context['city_items_counts']=city_items_counts
        return context       

    
class ItemDetailView(DetailView):
    model = Items
    template_name = 'item_detail.html'
    
    def get_context_data(self,**kwargs):
        context =super().get_context_data(**kwargs)
        #その品物のお気に入り数を取得
        item = self.get_object() #そのインスタンスを取得
        favorite_count = item.favorited_by.count()
        context['favorite_count']=favorite_count

        return context
    
        

    
#商品投稿用（画像複数アップお試し）
@login_required
def item_create(request):
    item_create_form = ItemCreateForm(request.POST or None)
    item_picture_create_form = ItemPicturesCreateForm(request.POST or None, request.FILES or None)
    context = {
        'item_create_form':item_create_form,
        'item_picture_create_form':item_picture_create_form
    }
    if item_create_form.is_valid() and item_picture_create_form.is_valid():
        
        #マイページ詳細情報が登録されていないときにエラーを返す
        user = request.user
        try:
            address = Addresses.objects.get(user=user)
            city = address.city
        except Addresses.DoesNotExist:
            city =None
            
        #cityが設定されていなかった場合にエラーメッセージを表示
        if city is None or city=="":
            item_create_form.add_error(None,"品物を投稿するには先にマイページからマイページ情報を更新してください")
            return render(request,'item_create.html',context)
        #Itemsのuserフィールドにrequest.userを入れて保存
        item_instance = item_create_form.save(commit=False)
        item_instance.user = request.user
        item_instance.save()

        #ItemPicturesに各フィールドをいれる
        upload_pictures = request.FILES.getlist('picture',) #複数挙げられた画像をリストとして取得
        for picture in upload_pictures:
            picture_instance = ItemPictures(
                picture = picture,
                #他のフィールドをいれる？
                user = request.user,
                item = item_instance
            )
            picture_instance.save()
        
        return redirect('boards:my_items')
    
    
    return render(request,'item_create.html',context)

#自分の投稿商品一覧ページ用

class MyItemsView(ListView):
    model = Items
    template_name = 'my_items.html'
    paginate_by = 6

    def get_queryset(self):
        qs = super(MyItemsView,self).get_queryset()
        qs = qs.filter(user_id=self.request.user)
        qs = qs.order_by('-updated_at')
        return qs
    
#商品削除

class MyItemDeleteView(DeleteView):
    model = Items
    template_name = 'item_delete.html'
    success_url = reverse_lazy('boards:my_items')
    
#商品編集
@login_required
def my_item_edit(request,item_id):
    item = get_object_or_404(Items, item_id=item_id)

    item_edit_form = ItemEditForm(request.POST or None,instance=item) #instanceを指定することでDBから情報を取ってきてフォームに入力された状態にする
    item_picture_edit_form = ItemPictureEditForm(request.POST or None, request.FILES or None)
    if item_edit_form.is_valid() and item_picture_edit_form.is_valid():
        ItemPictures.objects.filter(item=item_id).delete() #DBの画像を削除
        
        item_instance = item_edit_form.save(commit=False)
        #複数アップロードされた画像をリストとして取得
        upload_pictures = request.FILES.getlist('picture',)
        for picture in upload_pictures:
            #ItemPicturesのitemフィールドにItemsのインスタンスを入れる。userもいれる
            item_picture_instance = ItemPictures(
                picture = picture,
                user = request.user,
                item = item_instance
            )
            item_picture_instance.save()
            item_edit_form.save()
        # item_pictures_instance = item_picture_edit_form.save(commit=False)
        # item_pictures_instance.item = item_instance #itemにItemsインスタンスを
        # item_pictures_instance.user = request.user #userにログイン中のユーザを
        messages.info(request,'商品情報を更新しました！')
        return redirect('boards:my_items')


    return render(request,'item_edit.html',context={
        'item_edit_form':item_edit_form,
        'item_picture_edit_form':item_picture_edit_form,


    })
    
#問い合わせページ
class ContactFormView(LoginRequiredMixin,CreateView):
    model = Contact
    template_name = 'item_contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('boards:item_contact_result')
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        try:
            #URLパラメータからitem_idを取得してそのItemsのインスタンスを取得
            item_id = self.kwargs.get('item_id')
        except Items.DoesNotExist:
            item_id=None
        item =Items.objects.get(item_id=item_id)
        context['user']=self.request.user
        context['item']=item
        return context
    
    def form_valid(self,contact_form):
        item_id = self.kwargs.get('item_id')
        item = get_object_or_404(Items,item_id=item_id)
        contact_form.instance.item = item
        contact_form.instance.from_user = self.request.user
        contact_form.instance.to_user = item.user
        
        #メールをおくる（おためし）
        subject="タダデス：品物へのお問い合わせ" #日本語名だとコンソール上でsubjectは文字化けしてしまう
        message=f"""
こんにちは！タダデス事務局です！
あなたの品物へのお問い合わせがとどきました！
        
お問い合わせのあった品物：{item.name}
http://127.0.0.1:8000/boards/item_detail/{item.item_id}/
お問い合わせ内容：{contact_form.instance.content}
        
お問い合わせユーザ名：{self.request.user.username}
http://127.0.0.1:8000/accounts/user_detail/{self.request.user.user_id}/
        
相手方のメールアドレス：{self.request.user.email}
        
以降は上記のメールアドレスにて直接相手方とご連絡いただき、取引を進めていただきますようお願い致します。
     
ログインする
http://127.0.0.1:8000/accounts/login/

-----------------       
タダデス事務局

-----------------
このメールに返信されてもご対応できかねますのでご了承ください。

"""
        from_email="sample1@gmail.com"
        to_email = contact_form.instance.to_user.email #相手のメールアドレス
        recipient_list=[
            to_email
        ]#宛先のアドレス
        send_mail(subject,message,from_email,recipient_list)

        response = super().form_valid(contact_form)       
        return response
  
class ContactResultView(TemplateView):
    template_name='item_contact_result.html'
    
    
#お気に入り機能
@login_required
def toggle_favorite(request,item_id):
    item = get_object_or_404(Items, item_id=item_id)
    
    #ユーザがお気に入りに登録しているかのチェック
    if request.user in item.favorited_by.all():
        item.favorited_by.remove(request.user)
        is_favorite = False
    else:
        item.favorited_by.add(request.user)
        is_favorite = True
        
    item.save()
    
    #JsonResponseをつかってTrueまたはFalseをJSON形式で返す
    # return JsonResponse({'is_favorite':is_favorite})
    return redirect('boards:favorite_list')

#お気に入り一覧ページ
@login_required
def favorite_list(request):
    user = request.user
    #userからの逆参照なのでrelated_nameを使って取得できる
    favorite_items = user.favorite_items.all()
    return render(request, 'favorite_list.html', {'favorite_items': favorite_items})

#エラーハンドリング
def page_not_found(request,exception):
    return render(request,'404.html',status=404)
