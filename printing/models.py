from django.db import models
from slugify import slugify
from django.utils import timezone

def generate_unique_slug(instance, field_value, slug_field_name='slug'):
    slug = slugify(field_value)
    ModelClass = instance.__class__
    unique_slug = slug
    num = 1
    while ModelClass.objects.filter(**{slug_field_name: unique_slug}).exclude(pk=instance.pk).exists():
        unique_slug = f"{slug}-{num}"
        num += 1
    return unique_slug

class ServiceCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # chỉ tạo nếu slug chưa có
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Danh mục dịch vụ"
        verbose_name_plural = "Danh mục dịch vụ"
        ordering = ['name']

class Service(models.Model):
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_popular = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:  # chỉ tạo nếu slug chưa có
            self.slug = generate_unique_slug(self, self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PriceTable(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='prices')
    unit = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.service.name} - {self.unit}: {self.price:,} VND"

class Order(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveIntegerField()

    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    order_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    status_choices = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('processing', 'Đang xử lý'),
        ('completed', 'Hoàn thành'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_code:
            today_str = timezone.now().strftime("%Y%m%d")
            today_orders = Order.objects.filter(order_code__startswith=today_str).count() + 1
            self.order_code = f"{today_str}-{today_orders}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"#{self.id} - {self.customer_name} - {self.service.name}"
