from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, DetailView, CreateView,TemplateView,FormView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from event_system.forms import BookingForm, HallForm, PaymentForm
from .models import Booking, Hall, Payment
from django.utils.timezone import localtime, now
from django.utils.dateparse import parse_datetime


class HomeView(ListView):
    model = Hall
    template_name = "event/home.html"
    context_object_name = "halls"

    def get_queryset(self):
        return Hall.objects.prefetch_related("images", "amenities").all()

from datetime import timedelta

class DetailView(DetailView):
    model = Hall
    template_name = "event/detail/detail.html"
    context_object_name = "hall"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hall = self.get_object()

        bookings = hall.bookings.all()
        booked_dates = set()

        for booking in bookings:
            if not booking.start_datetime or not booking.end_datetime:
                continue

            current_date = booking.start_datetime
            while current_date < booking.end_datetime: 
                booked_dates.add(current_date)
                current_date += timedelta(days=1)

        context['booked_dates'] = sorted(date.strftime('%Y-%m-%d') for date in booked_dates)
        return context

class BookingCreateView(FormView):
    form_class = BookingForm
    template_name = "event/detail/booking-form.html"

    def dispatch(self, request, *args, **kwargs):
        self.hall = get_object_or_404(Hall, pk=self.kwargs["hall_id"])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form_data = form.cleaned_data.copy()

        # Convert datetime objects to strings for session storage
        form_data["start_datetime"] = form_data["start_datetime"].isoformat()
        form_data["end_datetime"] = form_data["end_datetime"].isoformat()
        form_data["hall_id"] = self.hall.id

        self.request.session["temp_booking_data"] = form_data
        return redirect(reverse("payment_create"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hall"] = self.hall
        return context

    
from django.http import JsonResponse
from datetime import datetime

def check_availability(request):
    if request.method == 'POST':
        hall_id = request.POST.get('hall_id')
        start = request.POST.get('start_datetime')
        end = request.POST.get('end_datetime')

        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
        except Exception:
            return JsonResponse({'available': False, 'error': 'Invalid date format'})

        overlapping = Booking.objects.filter(
            hall_id=hall_id,
            start_datetime__lt=end_dt,
            end_datetime__gt=start_dt
        ).exists()

        return JsonResponse({'available': not overlapping})

class PaymentCreateView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'event/detail/payment.html'
    success_url = reverse_lazy('payment_success')

    def get_initial(self):
        initial = super().get_initial()
        booking_data = self.request.session.get("temp_booking_data")

        if booking_data:
            hall_id = booking_data.get("hall_id")
            hall = Hall.objects.filter(id=hall_id).first()
            start = parse_datetime(booking_data.get("start_datetime"))
            end = parse_datetime(booking_data.get("end_datetime"))

            total_price = 0
            self.hall_name = hall.name if hall else None
            self.customer_email = booking_data.get("customer_email")

            if hall and start and end:
                duration = end - start
                days = duration.days
                if duration.seconds > 0:
                    days += 1
                if days <= 0:
                    days = 1
                total_price = days * hall.price_per_day

            self.total_price = total_price
            initial["hall"] = hall_id
            initial["email"] = self.customer_email
            initial["amount"] = total_price

        return initial

    def form_valid(self, form):
        booking_data = self.request.session.get("temp_booking_data")
        if not booking_data:
            return redirect("booking_create")

        start = parse_datetime(booking_data.get("start_datetime"))
        end = parse_datetime(booking_data.get("end_datetime"))
        hall = get_object_or_404(Hall, id=booking_data["hall_id"])

        booking = Booking.objects.create(
            hall=hall,
            customer_name=booking_data["customer_name"],
            customer_email=booking_data["customer_email"],
            start_datetime=start,
            end_datetime=end,
            status='pending',
        )
      

        payment = form.save(commit=False)
        payment.booking = booking
        payment.amount = booking.total_price
        payment.save()

        # Save for payment success
        self.request.session['payment_success_booking_id'] = booking.id
        self.request.session['payment_success_payment_id'] = payment.id
        self.request.session.pop('temp_booking_data', None)

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hall_name"] = getattr(self, 'hall_name', None)
        context["total_price"] = getattr(self, 'total_price', None)
        context["customer_email"] = getattr(self, 'customer_email', None)
        return context


class PaymentSuccessView(TemplateView):
    template_name = 'event/detail/payment_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_datetime'] = localtime(now())

        booking_id = self.request.session.pop('payment_success_booking_id', None)
        payment_id = self.request.session.pop('payment_success_payment_id', None)

        if booking_id:
            try:
                booking = Booking.objects.select_related('hall').get(id=booking_id)
                context['booking'] = booking
                context['hall'] = booking.hall
            except Booking.DoesNotExist:
                context['booking'] = None
                context['hall'] = None
        else:
            context['booking'] = None
            context['hall'] = None

        if payment_id:
            try:
                payment = Payment.objects.get(id=payment_id)
                context['payment'] = payment
            except Payment.DoesNotExist:
                context['payment'] = None
        else:
            context['payment'] = None

        return context
    
class HallCreateView(CreateView):
    model=Hall
    template_name='event/operations/add_hall.html'
    form_class=HallForm
    success_url='/'    

    def form_valid(self, form):
        form.instance.created_by=self.request.user
        return super().form_valid(form)
    
class ShowTableData(ListView):
    model=Booking
    template_name='event/operations/datatable.html'
    context_object_name='booking'   

    def get_queryset(self):
        return Booking.objects.filter(status="accepted").order_by('-start_datetime')
    
class RegisterView(FormView):
    template_name = 'event/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login') 

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
from django.contrib.auth.decorators import user_passes_test
def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_required
def accept_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'accepted'
    booking.save()
    return redirect('booking_list')

@superuser_required
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('booking_list') 

class BookingListView(ListView):
    model=Booking
    template_name='event/detail/booking_list.html'
    context_object_name='book'
    def get_queryset(self):
        return Booking.objects.filter(status="pending")


