from django.db import models
from accounts.models import User
from django.db.models import Q

#検索窓用モデル
class ItemsQuerySet(models.QuerySet):
    def search(self,query=None):
        qs = self #object.allとかそれらを含む
        if query is not None:
            or_lookup = ( #qオブジェクトを作成（なにで検索可能にするか）
                Q(name__icontains=query)|
                Q(comment__icontains=query)|
                Q(category__icontains=query)|
                Q(user__addresses__city__icontains=query)|
                Q(user__addresses__address__icontains=query)
            )
            qs=qs.filter(or_lookup).distinct()#重複を除く
        return qs.order_by("-created_at")
    
#検索窓用Itemsモデルマネージャー
class ItemsModelManager(models.Manager):
    def get_queryset(self):
        return ItemsQuerySet(self.model,using=self._db)
    
    def search(self,query=None):
        return self.get_queryset().search(query=query)

class Items(models.Model):
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
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    comment = models.TextField(max_length=1000)
    favorited_by = models.ManyToManyField(User,related_name='favorite_items',blank=True)
    category = models.CharField(max_length=30,choices=CATEGORY_NAME)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    
    objects=ItemsModelManager()
    
    class Meta:
        verbose_name = '出品'
        verbose_name_plural = '出品一覧'
        
    def __str__(self):
        return self.name
    
class ItemPictures(models.Model):
    item_picture_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='item_pictures/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = '出品写真'
        verbose_name_plural = '出品写真一覧'
        
    def __str__(self):
        return str(self.item.name)

#問い合わせフォーム用モデル
class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Items,on_delete=models.CASCADE)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='from_user')
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='to_user')
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return 'from:'+self.from_user.email+' '+'to:'+self.to_user.email
    
    class Meta:
        verbose_name='お問い合わせ'
        verbose_name_plural='問い合わせ一覧'
        db_table='contacts'