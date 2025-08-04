# Create your models here.
from django.db import models
from cloudinary.models import CloudinaryField
from core.utils.cloudinary_helpers import unique_slugify

class Service(models.Model):
    tendv = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    hinh = CloudinaryField('Hình Ảnh', blank=True, null=True, folder='sieutoc')
    banner = CloudinaryField('Banner', blank=True, null=True, folder='sieutoc')
    phobien = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        

        if not self.slug and self.tendv:
            self.slug = unique_slugify(self, self.tendv)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tendv
    class Meta:
        verbose_name = "Dịch Vụ"
        verbose_name_plural = "Dịch Vụ"

class Product(models.Model):
    tensp = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    mota = models.TextField(blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="products")
    hinh = CloudinaryField('Hình Ảnh', blank=True, null=True, folder='sieutoc')    
    phobien = models.BooleanField(default=False)
    gia = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    donvi = models.CharField(max_length=50, default="cái")
    def save(self, *args, **kwargs):
        

        if not self.slug and self.tensp:
            self.slug = unique_slugify(self, self.tensp)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tensp
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"