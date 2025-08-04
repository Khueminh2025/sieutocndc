import cloudinary.api
import cloudinary.exceptions

from slugify import slugify


def unique_slugify(instance, value, slug_field_name='slug'):
    """
    Tạo slug duy nhất cho instance từ value (thường là name).
    Tự động thêm -1, -2, ... nếu slug đã tồn tại.
    """
    base_slug = slugify(value)
    slug = base_slug
    counter = 1
    ModelClass = instance.__class__

    while ModelClass.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug





def generate_unique_public_id(base_folder, slug):
    """
    Tạo public_id từ slug, thêm hậu tố nếu đã tồn tại.
    """
    base_id = f"{base_folder}/{slug}"
    public_id = base_id
    suffix = 1

    while True:
        try:
            # Kiểm tra ảnh đã tồn tại chưa trên Cloudinary
            cloudinary.api.resource(public_id)
            # Nếu tồn tại thì thêm hậu tố
            public_id = f"{base_id}-{suffix}"
            suffix += 1
        except cloudinary.exceptions.NotFound:
            # Nếu chưa tồn tại thì dùng được
            break

    return public_id


from cloudinary.uploader import upload
from slugify import slugify

def upload_image_to_cloudinary(image_file, folder, key):
    """
    Upload ảnh lên Cloudinary theo folder + key slug.
    Trả về secure_url nếu thành công.
    """
    public_id = f"{folder}/{slugify(key)}"
    result = upload(
        image_file,
        public_id=public_id,
        folder=folder,
        overwrite=True,
        resource_type='image'
    )
    return result.get("secure_url")



def get_image_url_by_slug(loai: str, slug: str) -> str | None:
    public_id = f'sieutoc/{loai}/{slug}'
    try:
        result = cloudinary.api.resource(public_id, resource_type='image')
        return result.get('secure_url')
    except cloudinary.exceptions.NotFound:
        return None