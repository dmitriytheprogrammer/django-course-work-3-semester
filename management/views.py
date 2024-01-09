from django.db.models import Q
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from .models import Product, Category, Category_Product, Warehouse, Order, Delivery, Supplier
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime

from .pagination import ProductsPagination
from .serializers import CategorySerializer, WarehouseSerializer, ProductSerializer, OrderSerializer, \
  DeliverySerializer, SupplierSerializer


def index(request):
    num_products = Product.objects.all().count()
    num_categories = Category.objects.all().count()
    num_suppliers = Supplier.objects.all().count()
    num_orders = Order.objects.all().count()
    num_deliveries = Delivery.objects.all().count()
    num_warehouses = Warehouse.objects.all().count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    return render(
        request,
        'index.html',
        context={
            'num_products': num_products,
            'num_categories': num_categories,
            'num_suppliers': num_suppliers,
            'num_orders': num_orders,
            'num_deliveries': num_deliveries,
            'num_warehouses': num_warehouses,
            'num_visits': num_visits,
        },
    )


# PRODUCT
class ProductListView(ListView):
    model = Product
    paginate_by = 10

class ProductDetailView(DetailView):
    model = Product

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'summary', 'price', 'quantity', 'warehouse_id']
    permission_required = 'management.can_mark_returned'

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'summary', 'price', 'quantity', 'warehouse_id']
    permission_required = 'management.can_mark_returned'

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products')
    permission_required = 'management.can_mark_returned'

# CATEGORY
class CategoryListView(ListView):
    model = Category
    paginate_by = 10

class CategoryDetailView(DetailView):
    model = Category

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name', 'summary']
    permission_required = 'management.can_mark_returned'

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name', 'summary']
    permission_required = 'management.can_mark_returned'

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('categories')
    permission_required = 'management.can_mark_returned'

# WAREHOUSE
class WarehouseListView(ListView):
    model = Warehouse
    paginate_by = 10
    template_name = 'warehouse_list.html'
    context_object_name = 'warehouse_list'

class WarehouseDetailView(DetailView):
    model = Warehouse

class WarehouseCreateView(CreateView):
    model = Warehouse
    fields = ['name', 'address']
    permission_required = 'management.can_mark_returned'

class WarehouseUpdateView(UpdateView):
    model = Warehouse
    fields = ['name', 'address']
    permission_required = 'management.can_mark_returned'

class WarehouseDeleteView(DeleteView):
    model = Warehouse
    success_url = reverse_lazy('warehouses')
    permission_required = 'management.can_mark_returned'

# ORDER
class OrderListView(ListView):
    model = Order
    paginate_by = 10
    template_name = 'order_list.html'
    context_object_name = 'order_list'

class OrderDetailView(DetailView):
    model = Order

class OrderCreateView(CreateView):
    model = Order
    fields = ['product', 'user', 'quantity', 'status']
    permission_required = 'management.can_mark_returned'

class OrderUpdateView(UpdateView):
    model = Order
    fields = ['product', 'user', 'quantity', 'status']
    permission_required = 'management.can_mark_returned'

class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('orders')
    permission_required = 'management.can_mark_returned'

# DELIVERY
class DeliveryListView(ListView):
    model = Delivery
    paginate_by = 10
    template_name = 'delivery_list.html'
    context_object_name = 'delivery_list'

class DeliveryDetailView(DetailView):
    model = Delivery

class DeliveryCreateView(CreateView):
    model = Delivery
    fields = ['product', 'supplier', 'quantity', 'date']
    permission_required = 'management.can_mark_returned'

class DeliveryUpdateView(UpdateView):
    model = Delivery
    fields = ['product', 'supplier', 'quantity', 'date']
    permission_required = 'management.can_mark_returned'

class DeliveryDeleteView(DeleteView):
    model = Delivery
    success_url = reverse_lazy('deliveries')
    permission_required = 'management.can_mark_returned'

# SUPPLIER
class SupplierListView(ListView):
    model = Supplier
    paginate_by = 10
    template_name = 'supplier_list.html'
    context_object_name = 'supplier_list'

class SupplierDetailView(DetailView):
    model = Supplier

class SupplierCreateView(CreateView):
    model = Supplier
    fields = ['name', 'contact', 'address', 'tel']
    permission_required = 'management.can_mark_returned'

class SupplierUpdateView(UpdateView):
    model = Supplier
    fields = ['name', 'contact', 'address', 'tel']
    permission_required = 'management.can_mark_returned'

class SupplierDeleteView(DeleteView):
    model = Supplier
    success_url = reverse_lazy('suppliers')
    permission_required = 'management.can_mark_returned'


class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer


class WarehouseViewSet(viewsets.ModelViewSet):
  queryset = Warehouse.objects.all()
  serializer_class = WarehouseSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductsPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'summary']

    @action(methods=['GET'], detail=False)
    def filter_products(self, request):
        min_price = request.query_params.get('price')
        if min_price:
            queryset = Product.objects.filter(
                ~Q(price__lt=min_price) & Q(quantity__gt=0) | (Q(warehouses__id=1) & ~Q(price__lt=min_price))
            )
        else:
            queryset = Product.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = OrderSerializer
  filter_backends = [DjangoFilterBackend]
  filterset_fields = ['status']

  @action(methods=['GET'], detail=False)
  def filter_orders(self, request):
      min_quantity = request.query_params.get('quantity')
      queryset = Order.objects.filter(
          (Q(quantity__gte=min_quantity) & ~Q(status='CANCELLED')) | Q(status='PENDING')
      )

      serializer = self.get_serializer(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

  @action(methods=['POST'], detail=True)
  def mark_order_as_shipped(self, request, pk=None):
      order = self.get_object()

      order.status = 'SHIPPED'
      order.save()

      serializer = self.get_serializer(order)
      return Response(serializer.data, status=status.HTTP_200_OK)


class DeliveryViewSet(viewsets.ModelViewSet):
  queryset = Delivery.objects.all()
  serializer_class = DeliverySerializer


class SupplierViewSet(viewsets.ModelViewSet):
  queryset = Supplier.objects.all()
  serializer_class = SupplierSerializer
