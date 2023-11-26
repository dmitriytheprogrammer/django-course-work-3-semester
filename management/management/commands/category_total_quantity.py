from django.core.management.base import BaseCommand
from management.models import Category, ProductWarehouse
from django.db.models import Sum



class Command(BaseCommand):
    help = 'Prints the total quantity of products in the warehouse for a given category'

    def add_arguments(self, parser):
        parser.add_argument('category_id', type=int, help='ID of the category')

    def handle(self, *args, **options):
        category_id = options['category_id']

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Category "{category_id}" does not exist'))
            return

        total_quantity = ProductWarehouse.objects.filter(
            product__categories=category
        ).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0

        self.stdout.write(self.style.SUCCESS(f'Total quantity of products in the warehouse for category "{category_id}": {total_quantity}'))
