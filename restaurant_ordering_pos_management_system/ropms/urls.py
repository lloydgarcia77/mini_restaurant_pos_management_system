from django.urls import path
from ropms import views

app_name = "ropms"

urlpatterns = [
    path('', views.index_client, name="index_client"),
    path('registration/', views.registration, name="registration"),
    path('table-selection/', views.table_selection, name="table_selection"),
    path('cancel-table-selection/delete/<int:id>/', views.cancel_table_selection, name="cancel_table_selection"),
    path('menu-selection/<int:id>/', views.menu_selection, name="menu_selection"),
    path('table-selection/menu-selection/menu-detail/<int:id>/<int:tid>/', views.menu_detail, name="menu_detail"),
    path('table-selection/menu-selection/cart/<int:id>/<int:tid>/', views.cart, name="cart"),
    path('table-selection/menu-selection/cart/add-to-cart/<int:id>/<int:mid>/', views.add_item_to_cart, name="add_item_to_cart"),
    path('table-selection/menu-selection/cart/update-to-cart/<int:mid>/', views.update_item_to_cart, name="update_item_to_cart"),
    path('table-selection/menu-selection/cart/delete-from-cart/<int:cid>/', views.delete_item_from_the_cart, name="delete_item_from_the_cart"),
    path('checkout/', views.checkout, name="checkout"),


    
]