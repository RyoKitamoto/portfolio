from django.urls import path
from .views import TopView,ItemDetailView,item_create,MyItemsView,MyItemDeleteView,my_item_edit,ContactFormView,ContactResultView,toggle_favorite,favorite_list

app_name='boards'

urlpatterns=[
    path('top/',TopView.as_view(),name='top'),
    path('item_detail/<int:pk>/',ItemDetailView.as_view(),name='item_detail'),
    path('item_create/',item_create,name='item_create'),
    path('my_items/',MyItemsView.as_view(),name='my_items'),
    path('item_delete/<int:pk>/',MyItemDeleteView.as_view(),name='item_delete'),
    path('item_edit/<int:item_id>/',my_item_edit,name='item_edit'),
    path('item_contact/<int:item_id>/',ContactFormView.as_view(),name='item_contact'),
    path('item_contact_result/',ContactResultView.as_view(),name='item_contact_result'),
    path('toggle_favorite/<int:item_id>/',toggle_favorite,name='toggle_favorite'),
    path('favorite_list/',favorite_list,name='favorite_list'),
    #path('ajax_selected_city/',ajax_selected_city,name='ajax_selected_city'),
]