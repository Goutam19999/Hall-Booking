from django.urls import path

from event_system import views

urlpatterns = [
    path("", views.HomeView.as_view(),name='home'),
    path("hall-detail/<int:pk>/" , views.DetailView.as_view() , name="hall-detail"),
    path('bookings/create/<int:hall_id>/', views.BookingCreateView.as_view(), name='create_booking'),
    path('check-availability/', views.check_availability, name='check_availability'),
    path('payment/', views.PaymentCreateView.as_view(), name='payment_create'),
    path('payment-succes/',views.PaymentSuccessView.as_view(),name='payment_success'),
    path('add-hall/',views.HallCreateView.as_view(),name='add-hall'),
    path('show-tabledata/',views.ShowTableData.as_view(),name='show-table-data'),
    path('register/',views.RegisterView.as_view(), name='register'),
    path('booking/<int:booking_id>/accept/', views.accept_booking, name='accept_booking'),
    path('booking/<int:booking_id>/reject/', views.reject_booking, name='reject_booking'),
    path('booking_list/',views.BookingListView.as_view(),name='booking_list'),

]