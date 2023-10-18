from django import forms
from .models import Items,ItemPictures,Contact

#商品新規投稿フォーム1
class ItemCreateForm(forms.ModelForm):
    CATEGORY_NAME=(
        ('家具','家具'),
        ('家電','家電'),
        ('自転車','自転車'),
        ('楽器','楽器'),
        ('生活雑貨','生活雑貨'),
        ('子供用品','子供用品'),
        ('ホビー、ゲーム','ホビー、ゲーム'),
        ('服/ファッション','服/ファッション'),
        ('靴/バック','靴/バック'),
        ('コスメ/ヘルスケア','コスメ/ヘルスケア'),
        ('食品','食品'),
        ('スポーツ','スポーツ'),
        ('その他','その他'),
    )
    
    name = forms.CharField(label='アイテム名',max_length=100)
    comment = forms.CharField(
        label='コメント',
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'placeholder':'魅力的なアイテム説明を書こう！',
            }
        )
    )
    category = forms.ChoiceField(label='カテゴリー',choices=CATEGORY_NAME)
    
    class Meta:
        model = Items
        fields = ('name','comment','category',)
        
#商品新規投稿フォーム2
class ItemPicturesCreateForm(forms.ModelForm):
    picture = forms.ImageField(label='アイテム画像',
                               widget=forms.FileInput(attrs={'multiple':'True'}),)
    
    class Meta:
        model = ItemPictures
        fields = ('picture',)
        
#商品編集フォーム1
class ItemEditForm(forms.ModelForm):
    CATEGORY_NAME=(
        ('家具','家具'),
        ('家電','家電'),
        ('自転車','自転車'),
        ('楽器','楽器'),
        ('生活雑貨','生活雑貨'),
        ('子供用品','子供用品'),
        ('ホビー、ゲーム','ホビー、ゲーム'),
        ('服/ファッション','服/ファッション'),
        ('靴/バック','靴/バック'),
        ('コスメ/ヘルスケア','コスメ/ヘルスケア'),
        ('食品','食品'),
        ('スポーツ','スポーツ'),
        ('その他','その他'),
    )
    category = forms.ChoiceField(label='カテゴリー',choices=CATEGORY_NAME,required=False)

    
    class Meta:
        model = Items
        fields = ('name','comment','category',)
        
#商品編集フォーム2
class ItemPictureEditForm(forms.ModelForm):
    picture = forms.ImageField(label='アイテム画像',
                               widget=forms.FileInput(attrs={'multiple':'True'}),)
    
    class Meta:
        model = ItemPictures
        fields = ('picture',)
        
#問い合わせフォーム
class ContactForm(forms.ModelForm):
    content = forms.CharField(
        label='お問い合わせ内容',
        max_length=1000,
        widget=forms.Textarea(
            attrs={
                'placeholder':'例：はじめまして！〇〇と申します。こちらの品物が気になっております。〇〇市にお住まいとのことなので〇〇（場所名）で受け渡しは可能でしょうか？もしよろしければ日程等調整させていただきたいのでご返信いただければ幸いです！よろしくお願いいたします。'
            }
        )
    )
    class Meta:
        model = Contact
        fields =('content',)
        
#検索窓フォーム
class ItemSearchForm(forms.Form):
    CATEGORY_NAME=[
        ('家具','家具'),
        ('家電','家電'),
        ('自転車','自転車'),
        ('楽器','楽器'),
        ('生活雑貨','生活雑貨'),
        ('子供用品','子供用品'),
        ('ホビー、ゲーム','ホビー、ゲーム'),
        ('服/ファッション','服/ファッション'),
        ('靴/バック','靴/バック'),
        ('コスメ/ヘルスケア','コスメ/ヘルスケア'),
        ('食品','食品'),
        ('スポーツ','スポーツ'),
        ('その他','その他'),
    ]
    search = forms.CharField(required=False,
                             widget=forms.TextInput(
            attrs={'placeholder':'フリーワード検索  例：吹田市　冷蔵庫など'}))
    category = forms.ChoiceField(
        required=False,
        choices=[('','全てのカテゴリー')] + CATEGORY_NAME
    )