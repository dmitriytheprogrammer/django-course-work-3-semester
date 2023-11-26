from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'deliveries', DeliveryViewSet)
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', views.index, name='index'),

    path('api/', include(router.urls)),

    path('warehouses/', WarehouseListView.as_view(), name='warehouse-list'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('deliveries/', DeliveryListView.as_view(), name='delivery-list'),
    path('suppliers/', SupplierListView.as_view(), name='supplier-list'),

    path('warehouse/', views.WarehouseListView.as_view(), name='warehouse-list'),
    path('warehouse/<int:pk>/', views.WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('order/', views.OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('delivery/', views.DeliveryListView.as_view(), name='delivery-list'),
    path('delivery/<int:pk>/', views.DeliveryDetailView.as_view(), name='delivery-detail'),
    path('supplier/', views.SupplierListView.as_view(), name='supplier-list'),
    path('supplier/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),

    path('product/', views.ProductListView.as_view(), name='product'),
    path('product/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/<int:pk>', views.CategoryDetailView.as_view(), name='category-detail'),
    path('product/', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/create/', ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('warehouses/', WarehouseListView.as_view(), name='warehouses'),
    path('warehouse/<int:pk>/', WarehouseDetailView.as_view(), name='warehouse-detail'),
    path('warehouse/create/', WarehouseCreateView.as_view(), name='warehouse-create'),
    path('warehouse/<int:pk>/update/', WarehouseUpdateView.as_view(), name='warehouse-update'),
    path('warehouse/<int:pk>/delete/', WarehouseDeleteView.as_view(), name='warehouse-delete'),
    path('orders/', OrderListView.as_view(), name='orders'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('order/create/', OrderCreateView.as_view(), name='order-create'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('order/<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),
    path('deliveries/', DeliveryListView.as_view(), name='deliveries'),
    path('delivery/<int:pk>/', DeliveryDetailView.as_view(), name='delivery-detail'),
    path('delivery/create/', DeliveryCreateView.as_view(), name='delivery-create'),
    path('delivery/<int:pk>/update/', DeliveryUpdateView.as_view(), name='delivery-update'),
    path('delivery/<int:pk>/delete/', DeliveryDeleteView.as_view(), name='delivery-delete'),
    path('suppliers/', SupplierListView.as_view(), name='suppliers'),
    path('supplier/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),
    path('supplier/create/', SupplierCreateView.as_view(), name='supplier-create'),
    path('supplier/<int:pk>/update/', SupplierUpdateView.as_view(), name='supplier-update'),
    path('supplier/<int:pk>/delete/', SupplierDeleteView.as_view(), name='supplier-delete'),
]
