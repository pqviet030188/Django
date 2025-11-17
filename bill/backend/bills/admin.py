from django.contrib import admin
from django.utils.html import format_html
from .models import Bill
from .models import BillImage
from .models import Instalment
# Register your models here.
class BillImageInline(admin.TabularInline):
    model = BillImage
    extra = 1
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px;" />', obj.image.url)
        return "(No image)"
    
    image_preview.short_description = "Preview"

class InstalmentInline(admin.TabularInline):
    model = Instalment
    extra = 1
    readonly_fields = ['instalment_preview']

    def instalment_preview(self, obj):
        if obj:
            return format_html('<p>{}</p>', str(obj))
        return "(No instalment)"
    
    instalment_preview.short_description = "Preview"

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('biller', 'amount', 'date', 'status')
    readonly_fields = ('status_context', )
    fields = ('biller', 'amount', 'date', 'status', 'status_context')
    inlines = [BillImageInline, InstalmentInline]