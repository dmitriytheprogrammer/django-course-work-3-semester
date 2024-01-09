from django import forms
from django.contrib import admin
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from import_export import resources, fields
from import_export.admin import ExportMixin
from import_export.formats import base_formats
from import_export.widgets import ForeignKeyWidget
from simple_history.admin import SimpleHistoryAdmin

from .models import Product, Category, Category_Product, Warehouse, Order, Delivery, Supplier, ProductWarehouse


class AdminModel(SimpleHistoryAdmin, admin.ModelAdmin):
    pass


class ProductResource(resources.ModelResource):

    class Meta:
        model = Product


class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category


class OrderResource(resources.ModelResource):
    user = fields.Field(
        column_name='user',
        attribute='user',
        widget=ForeignKeyWidget(User, field='username'))
    class Meta:
        model = Order


    def dehydrate_product(self, order):
        rounded_price = round(order.product.price, 2)
        return f"${rounded_price}"



class DeliveryResource(resources.ModelResource):
    class Meta:
        model = Delivery


class SupplierResource(resources.ModelResource):

    class Meta:
        model = Supplier


class WarehouseResource(resources.ModelResource):

    class Meta:
        model = Warehouse


class ProductForm(forms.ModelForm):
    warehouses = forms.ModelMultipleChoiceField(
        queryset=Warehouse.objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Warehouses', is_stacked=False),
        required=False,
        label='Warehouses'
    )

    class Meta:
        model = Product
        fields = '__all__'


class CategoryInline(admin.TabularInline):
    model = Category_Product
    extra = 1


@admin.register(Product)
class ProductAdmin(ExportMixin, AdminModel):
    list_display = ('name', 'summary', 'price', 'quantity', 'get_warehouse_names')
    list_filter = ('categories', 'warehouses')
    inlines = [CategoryInline]
    search_fields = ('name', 'summary')
    form = ProductForm
    filter_horizontal = ('warehouses',)
    readonly_fields = ('get_warehouse_names',)
    resource_class = ProductResource

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        warehouses = form.cleaned_data.get('warehouses')
        if warehouses is not None:
            for warehouse in warehouses:
                ProductWarehouse.objects.update_or_create(
                    product=obj,
                    warehouse=warehouse,
                    defaults={'quantity': obj.quantity}
                )

    def get_warehouse_names(self, obj):
        return ', '.join([str(warehouse) for warehouse in obj.warehouses.all()])
    get_warehouse_names.short_description = 'Warehouses'


    def get_export_formats(self):
        formats = (
            base_formats.CSV,
            base_formats.XLSX,
        )
        return [f for f in formats if f().can_export()]


@admin.register(Order)
class OrderAdmin(ExportMixin, AdminModel):
    list_display = ('id', 'product_link', 'user', 'quantity', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('product__name', 'user__username')

    fieldsets = (
        ('General Information', {
            'fields': ('product', 'user', 'quantity', 'date')
        }),
        ('Status Information', {
            'fields': ('status',)
        }),
    )

    readonly_fields = ('id', 'date', 'product_link')

    def product_link(self, obj):
        return format_html('<a href="{}">{}</a>', obj.product.get_absolute_url(), obj.product.name)
    product_link.short_description = 'Product'

    resource_class = OrderResource

    def get_export_queryset(self, request):
        return Order.objects.filter(status='DELIVERED')



@admin.register(Delivery)
class DeliveryAdmin(ExportMixin, AdminModel):
    list_display = ('product', 'supplier', 'quantity', 'date')
    list_filter = ('date',)
    resource_class = DeliveryResource


@admin.register(Supplier)
class SupplierAdmin(ExportMixin, AdminModel):
    list_display = ('name', 'contact', 'address', 'tel')
    resource_class = SupplierResource


@admin.register(Warehouse)
class WarehouseAdmin(ExportMixin, AdminModel):
    list_display = ('name', 'address')
    resource_class = WarehouseResource


@admin.register(ProductWarehouse)
class ProductWarehouseAdmin(AdminModel):
    list_display = ('product', 'warehouse', 'quantity')


admin.site.register(Category, AdminModel)
admin.site.register(Category_Product)
