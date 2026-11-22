from django.contrib import admin
from django.db.models import Sum, Count
from django.template.response import TemplateResponse
from django.urls import path
from .models import Cart, CartItem, Order, OrderItem, PaymentTransaction

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_brand', 'price', 'quantity', 'line_total')

class PaymentTransactionInline(admin.TabularInline):
    model = PaymentTransaction
    extra = 0
    readonly_fields = ('transaction_uuid', 'transaction_code', 'provider', 'amount', 'status', 'is_verified', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'phone', 'city', 'payment_method', 'payment_status', 'order_status', 'total_amount', 'created_at')
    list_filter = ('payment_status', 'order_status', 'payment_method', 'city', 'created_at')
    list_editable = ('order_status', 'payment_status')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'delivery_address')
    inlines = [OrderItemInline, PaymentTransactionInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard-reports/', self.admin_site.admin_view(self.dashboard_reports_view), name='orders_dashboard_reports'),
        ]
        return custom_urls + urls

    def dashboard_reports_view(self, request):
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(payment_status='PAID').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        pending_orders = Order.objects.filter(order_status='PLACED').count()
        delivered_orders = Order.objects.filter(order_status='DELIVERED').count()
        
        popular_products = OrderItem.objects.values('product_name').annotate(
            total_sold=Sum('quantity'),
            revenue=Sum('price')
        ).order_by('-total_sold')[:10]

        context = {
            **self.admin_site.each_context(request),
            'title': 'CURLIQUE Analytics & Order Reports',
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'delivered_orders': delivered_orders,
            'popular_products': popular_products,
        }
        return TemplateResponse(request, 'admin/orders_reports.html', context)

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_uuid', 'order', 'provider', 'amount', 'status', 'is_verified', 'created_at')
    list_filter = ('provider', 'status', 'is_verified')
    search_fields = ('transaction_uuid', 'transaction_code', 'order__order_number')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'total_items', 'subtotal', 'created_at')
