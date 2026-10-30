from datetime import date

from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking
from spots.models import Spot
from users.models import User


class BookingORMTests(TestCase):
    def setUp(self):
        self.spot = Spot.objects.create(
            number="A1",
            covered=True,
            daily_rate="500.00",
        )
        self.user = User.objects.create(
            name="Иван Иванов",
            phone="+79001111111",
        )
        self.today = date.today()

    def test_booking_list_filters_by_q(self):
        Booking.objects.create(
            spot=self.spot,
            user=self.user,
            start=self.today,
            end=self.today,
            is_cancelled=False,
        )

        response = self.client.get(
            reverse("bookings:list"),
            {"q": "A1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1")

    def test_statistics_counts_zero_for_spot_without_bookings(self):
        response = self.client.get(reverse("bookings:statistics"))

        self.assertEqual(response.status_code, 200)
        stats = list(response.context["statistics"])
        self.assertTrue(
            any(
                item["spot_number"] == "A1" and item["bookings_count"] == 0
                for item in stats
            )
        )

    def test_available_spots_excludes_active_booking(self):
        Booking.objects.create(
            spot=self.spot,
            user=self.user,
            start=self.today,
            end=self.today,
            is_cancelled=False,
        )

        response = self.client.get(
            reverse("spots:available"),
            {"date": self.today.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "A1")

    def test_cancelled_booking_does_not_block_spot(self):
        Booking.objects.create(
            spot=self.spot,
            user=self.user,
            start=self.today,
            end=self.today,
            is_cancelled=True,
        )

        response = self.client.get(
            reverse("spots:available"),
            {"date": self.today.isoformat()},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A1")

    def test_invalid_date_message(self):
        response = self.client.get(
            reverse("spots:available"),
            {"date": "not-a-date"},
        )

        self.assertContains(response, "Укажите корректную дату.")
