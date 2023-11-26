from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название категории товара")
    summary = models.TextField(max_length=1000, help_text="Введите краткое описание категории")

    history = HistoricalRecords()
    def get_absolute_url(self):
        return reverse('category-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Category_Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.category} - {self.product}"

    class Meta:
        verbose_name = 'Category_Product'
        verbose_name_plural = 'Categories_Products'


class Warehouse(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название склада")
    address = models.CharField(max_length=200, help_text="Введите адрес склада")
    history = HistoricalRecords()
    def get_absolute_url(self):
        return reverse('warehouse-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class ProductWarehouse(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Введите количество товара на складе", default=0)
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.product} - {self.warehouse}"

    class Meta:
        verbose_name = 'ProductWarehouse'
        verbose_name_plural = 'ProductWarehouses'


class Product(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название товара")
    summary = models.CharField(max_length=1000, help_text="Введите краткое описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Введите цену товара")
    quantity = models.PositiveIntegerField(help_text="Введите количество товара")
    warehouses = models.ManyToManyField(Warehouse, through=ProductWarehouse, related_name='products', help_text="Склады", blank=True)
    categories = models.ManyToManyField(Category, through=Category_Product, related_name='products', help_text="Категории", blank=True)
    history = HistoricalRecords()
    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        warehouses = self.warehouses.all()
        for warehouse in warehouses:
            ProductWarehouse.objects.update_or_create(
                product=self,
                warehouse=warehouse,
                defaults={'quantity': self.quantity}
            )


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Введите количество товара")
    date = models.DateField(auto_now_add=True, help_text="Время создания заказа")
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('order-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.product)


class Delivery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(help_text="Введите количество поставляемого товара")
    date = models.DateField(help_text="Выберите дату поставки")
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('delivery-detail', args=[str(self.id)])

    def __str__(self):
        return str(self.product)

    class Meta:
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'


class Supplier(models.Model):
    name = models.CharField(max_length=200, help_text="Введите наименование организации")
    contact = models.CharField(max_length=200, help_text="Введите контактное лицо")
    address = models.CharField(max_length=200, help_text="Введите адрес поставщика")
    tel = models.CharField(max_length=20, help_text="Введите номер телефона")
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse('supplier-detail', args=[str(self.id)])

    def __str__(self):
        return self.name
