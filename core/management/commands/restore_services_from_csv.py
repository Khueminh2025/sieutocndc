import csv
from django.core.management.base import BaseCommand
from services.models import Service, Product  # đổi lại nếu model của bạn nằm nơi khác
from core.utils.cloudinary_helpers import get_image_url_by_slug , generate_unique_public_id
from slugify import slugify
from pathlib import Path
import cloudinary.uploader

class Command(BaseCommand):
    help = "Import dịch vụ từ CSV và tự động gán hình ảnh từ Cloudinary"

    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    def handle(self, *args, **kwargs):
        file_path_dichvu = 'data/dichvu.csv'
        file_path_sanpham = 'data/sanpham.csv'
        image_dir = Path(kwargs.get('image_dir', 'data/images'))
        banner_dir = Path(kwargs.get('image_dir', 'data/banner'))
        hinh_dir = Path(kwargs.get('image_dir', 'data/dichvu'))
        image_index = 1
        if not Path(file_path_dichvu).exists():
            self.stdout.write(self.style.ERROR(f"Không tìm thấy file: {file_path_dichvu}"))
            return
        if not Path(file_path_sanpham).exists():
            self.stdout.write(self.style.ERROR(f"Không tìm thấy file: {file_path_sanpham}"))
            return

        with open(file_path_dichvu, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                tendv = row['tendv']
                slug = slugify(tendv)
                hinhanh_url = get_image_url_by_slug('service', slug)
                banner_url = get_image_url_by_slug('banner', slug)

                service, created = Service.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'tendv': tendv,
                        'hinh': hinhanh_url or '',
                        'banner': banner_url or ''
                    }
                )

                if not created:
                    # cập nhật nếu đã tồn tại
                    service.tendv = tendv
                    if hinhanh_url:
                        service.hinh = hinhanh_url
                    if banner_url:
                        service.banner = banner_url
                    service.save()

                hinh_existing_url = get_image_url_by_slug('service', slug)
                
                if hinh_existing_url:
                    service.hinh = hinh_existing_url
                    self.stdout.write(f"🔄 Dùng ảnh có sẵn trên Cloudinary cho `{slug}`")
                else:
                    hinh_path = hinh_dir / f"{count+1}.jpg"
                    if hinh_path.exists():
                        try:
                            result = cloudinary.uploader.upload(
                                str(hinh_path),
                                public_id=generate_unique_public_id('', slug),
                                folder='sieutoc/service',
                                overwrite=True,
                                resource_type='image'
                            )
                            service.hinh = result['secure_url']   
                            self.stdout.write(self.style.SUCCESS(f"🆕 Upload ảnh {count+1}.jpg -> {slug}"))
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"❌ Lỗi upload ảnh `{count+1}`: {e}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"⚠️ Không tìm thấy ảnh local: {count+1}"))
                    service.save()

                banner_existing_url = get_image_url_by_slug('banner', slug)

                if banner_existing_url:
                    service.banner = banner_existing_url
                    self.stdout.write(f"🔄 Dùng ảnh có sẵn trên Cloudinary cho `{slug}`")
                else:
                    banner_path = banner_dir / f"{count+1}.jpg"
                    if banner_path.exists():
                        try:
                            result = cloudinary.uploader.upload(
                                str(banner_path),
                                public_id=generate_unique_public_id('', slug),
                                folder='sieutoc/banner',
                                overwrite=True,
                                resource_type='image'
                            )
                            service.banner = result['secure_url']   
                            self.stdout.write(self.style.SUCCESS(f"🆕 Upload ảnh {count+1}.jpg -> {slug}"))
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"❌ Lỗi upload ảnh `{count+1}`: {e}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"⚠️ Không tìm thấy ảnh local: {count+1}"))
                    service.save()

                self.stdout.write(f"✅ {'Tạo' if created else 'Cập nhật'}: {slug}")
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Đã xử lý {count} dòng."))

        with open(file_path_sanpham, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0

            for row in reader:
                tensp = row['tensp']
                mo_ta = row.get('mo_ta', '').strip()
                donvitinh = row.get('donvitinh', '').strip()
                gia = int(row.get('gia', '0').strip())
                slug = slugify(tensp)
                service_id = row.get('dichvu')

                if not (tensp and service_id):
                    self.stdout.write(self.style.WARNING(f"Bỏ qua dòng thiếu thông tin: {row}"))
                    continue
                try:
                    service = Service.objects.get(id=service_id)
                except Service.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Dịch vụ không tồn tại: ID={service_id}"))
                    continue

                hinhanh_url = get_image_url_by_slug("products", slug)            


                # Tạo hoặc cập nhật product
                product, created = Product.objects.get_or_create(
                    slug=slug,
                    defaults={
                        'tensp': tensp,
                        'mota': mo_ta,
                        'gia': gia,
                        'donvi': donvitinh,
                        'service': service,
                        'phobien': False,
                        'hinh':hinhanh_url
                    }
                )

                if not created:
                    product.tensp = tensp
                    product.mota = mo_ta
                    product.gia = gia
                    product.donvi = donvitinh
                    product.service = service
                    if hinhanh_url:
                        product.hinhanh = hinhanh_url
                    product.save()

                existing_url = get_image_url_by_slug('products', slug)
                if existing_url:
                    product.hinh = existing_url
                    self.stdout.write(f"🔄 Dùng ảnh có sẵn trên Cloudinary cho `{slug}`")
                else:
                    image_path = image_dir / f"{image_index}.jpg"
                    if image_path.exists():
                        try:
                            result = cloudinary.uploader.upload(
                                str(image_path),
                                public_id=generate_unique_public_id('', slug),
                                folder='sieutoc/products',
                                overwrite=True,
                                resource_type='image'
                            )
                            product.hinh = result['secure_url']   
                            self.stdout.write(self.style.SUCCESS(f"🆕 Upload ảnh {image_index}.jpg -> {slug}"))
                        except Exception as e:
                            self.stdout.write(self.style.WARNING(f"❌ Lỗi upload ảnh `{image_path}`: {e}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"⚠️ Không tìm thấy ảnh local: {image_path}"))
                    image_index += 1 

                    product.save()
                

                # Gán dịch vụ liên quan
               

                self.stdout.write(f"{'✅ Tạo' if created else '🔁 Cập nhật'} sản phẩm: {slug}")
                count += 1

        self.stdout.write(self.style.SUCCESS(f"==> Đã xử lý {count} sản phẩm."))
