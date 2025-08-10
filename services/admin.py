from django.contrib import admin
import cloudinary.uploader
from core.utils.cloudinary_helpers import generate_unique_public_id, unique_slugify
from services.models import Service, Product

# Register your models here.
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['tendv','slug','phobien' ] 
    list_editable = ['phobien'] 

    def save_model(self, request, obj, form, change):
        # Giữ nguyên logic slug
        if not obj.slug:
            obj.slug = unique_slugify(obj, obj.tendv)
        # Upload ảnh lên Cloudinary nếu thay đổi
        if 'hinh' in form.changed_data and obj.hinh:
            upload_result = cloudinary.uploader.upload(
                obj.hinh,
                public_id=generate_unique_public_id('', obj.slug),
                folder='sieutoc/service',
                overwrite=True,
                resource_type='image'
            )
            obj.hinh = upload_result['secure_url']
        if 'banner' in form.changed_data and obj.banner:
            upload_result = cloudinary.uploader.upload(
                obj.banner,
                public_id=generate_unique_public_id('', obj.slug),
                folder='sieutoc/banner',
                overwrite=True,
                resource_type='image'
            )
            obj.banner = upload_result['secure_url']
        super().save_model(request, obj, form, change)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['tensp','slug','phobien' ]
    list_editable = ['phobien']

    def save_model(self, request, obj, form, change):
        # Giữ nguyên logic slug
        if not obj.slug:
            obj.slug = unique_slugify(obj, obj.tendv)
        # Upload ảnh lên Cloudinary nếu thay đổi
        if 'hinh' in form.changed_data and obj.hinh:
            upload_result = cloudinary.uploader.upload(
                obj.hinh,
                public_id=generate_unique_public_id('', obj.slug),
                folder='sieutoc/products',
                overwrite=True,
                resource_type='image'
            )
            obj.hinh = upload_result['secure_url']        
        super().save_model(request, obj, form, change)

