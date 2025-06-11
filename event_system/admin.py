from django.contrib import admin

from event_system.models import Amenity, Booking, Hall, HallImage, Payment

@admin.action(description='Accept selected bookings')
def accept_bookings(modeladmin, request, queryset):
    queryset.update(status='accepted')

@admin.action(description='Reject selected bookings')
def reject_bookings(modeladmin, request, queryset):
    queryset.delete()

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('hall', 'customer_name', 'start_datetime', 'status')
    list_filter = ('status',)
    exclude = ('status',)  # 👈 Hides 'status' field from the form
    actions = [accept_bookings, reject_bookings]

admin.site.register(Hall)
admin.site.register(HallImage)
admin.site.register(Amenity)
admin.site.register(Payment)

