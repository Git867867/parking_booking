from datetime import date, timedelta

from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking
from spots.models import Spot
from users.models import User


class BookingORMTests(TestCase):
    def setUp(self):
        self.spot = Spot.objects.create(number="A1", covered=True, daily_rate="500.00")
        self.user = User.objects.create(name="Иван Иванов", phone="+79001111111")
        self.today = date.today()

    def _create(self, status, start=None, end=None):
        return Booking.objects.create(
            spot=self.spot, user=self.user,
            start=start or self.today, end=end or self.today, status=status,
        )

    def test_booking_list_filters_by_q(self):
        self._create(Booking.Status.ACTIVE)
        response = self.client.get(reverse("bookings:list"), {"q": "A1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1")

    def test_statistics_counts_zero_for_spot_without_bookings(self):
        response = self.client.get(reverse("bookings:statistics"))
        self.assertEqual(response.status_code, 200)
        stats = list(response.context["statistics"])
        self.assertTrue(any(i["spot_number"] == "A1" and i["bookings_count"] == 0 for i in stats))

    def test_available_spots_excludes_active_booking(self):
        self._create(Booking.Status.ACTIVE)
        response = self.client.get(reverse("spots:available"), {"date": self.today.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "A1")

    def test_cancelled_booking_does_not_block_spot(self):
        self._create(Booking.Status.CANCELLED)
        response = self.client.get(reverse("spots:available"), {"date": self.today.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1")

    def test_completed_booking_does_not_block_spot(self):
        self._create(Booking.Status.COMPLETED)
        response = self.client.get(reverse("spots:available"), {"date": self.today.isoformat()})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1")

    def test_invalid_date_message(self):
        response = self.client.get(reverse("spots:available"), {"date": "not-a-date"})
        self.assertContains(response, "Укажите корректную дату.")

    def test_manager_methods(self):
        self._create(Booking.Status.ACTIVE)
        self._create(Booking.Status.CANCELLED)
        self._create(Booking.Status.COMPLETED)
        self.assertEqual(Booking.objects.count(), 3)
        self.assertEqual(Booking.objects.active().count(), 1)
        self.assertEqual(Booking.objects.cancelled().count(), 1)
        self.assertEqual(Booking.objects.completed().count(), 1)
        self.assertEqual(Booking.objects.for_date(self.today).count(), 3)
        self.assertEqual(Booking.objects.active().for_date(self.today).count(), 1)

    def test_statistics_status_counts(self):
        self._create(Booking.Status.ACTIVE)
        self._create(Booking.Status.CANCELLED)
        self._create(Booking.Status.COMPLETED)
        response = self.client.get(reverse("bookings:statistics"))
        counts = response.context["status_counts"]
        self.assertEqual(counts["total_bookings"], 3)
        self.assertEqual(counts["active_bookings"], 1)
        self.assertEqual(counts["cancelled_bookings"], 1)
        self.assertEqual(counts["completed_bookings"], 1)

    def test_booking_detail_shows_status(self):
        booking = self._create(Booking.Status.CANCELLED)
        response = self.client.get(reverse("bookings:detail", kwargs={"booking_id": booking.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Отменено")

    def test_pagination_keeps_spot_filter(self):
        for i in range(7):
            day = self.today + timedelta(days=i)
            self._create(Booking.Status.ACTIVE, start=day, end=day)
        response = self.client.get(reverse("bookings:list"), {"spot": str(self.spot.pk), "page": "2"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page_obj"].number, 2)
        self.assertEqual(len(response.context["page_obj"].object_list), 2)
        self.assertContains(response, "A1")