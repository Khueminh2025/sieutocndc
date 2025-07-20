from django.shortcuts import render, get_object_or_404, redirect
from .models import ServiceCategory, Service, PriceTable, Order
from .forms import OrderForm

def home(request):
    categories = ServiceCategory.objects.all()
    popular_services = Service.objects.filter(is_popular=True)
    return render(request, 'printing/home.html', {
        'categories': categories,
        'popular_services': popular_services,
    })
    
# ➡️ Trang dịch vụ theo danh mục
def category_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug)
    services = category.services.all()
    return render(request, 'printing/category_detail.html', {
        'category': category,
        'services': services,
    })

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    prices = PriceTable.objects.filter(service=service)
    return render(request, 'printing/service_detail.html', {
        'service': service,
        'prices': prices,
    })

def order_create(request, slug):
    service = get_object_or_404(Service, slug=slug)
    prices = service.prices.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.service = service
            order.unit = request.POST.get('unit')

            selected_price = prices.filter(unit=order.unit).first()
            if selected_price:
                order.total_price = selected_price.price * order.quantity
            else:
                order.total_price = 0

            order.save()
            return redirect('payment_page', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'printing/order_create.html', {
        'service': service,
        'prices': prices,
        'form': form,
    })

def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    # QR thanh toán có thể là ảnh tĩnh trong static hoặc dùng API tạo QR
    return render(request, 'printing/payment_page.html', {
        'order': order
    })

def order_tracking(request, order_code):
    order = get_object_or_404(Order, order_code=order_code)
    return render(request, 'printing/order_tracking.html', {
        'order': order
    })

def order_tracking_entry(request):
    order = None
    error = None

    if request.method == 'POST':
        order_code = request.POST.get('order_code')
        phone = request.POST.get('phone')

        try:
            order = Order.objects.get(order_code=order_code, phone=phone)
        except Order.DoesNotExist:
            error = "Không tìm thấy đơn hàng. Vui lòng kiểm tra lại mã đơn và số điện thoại."

    return render(request, 'printing/order_tracking_entry.html', {
        'order': order,
        'error': error
    })