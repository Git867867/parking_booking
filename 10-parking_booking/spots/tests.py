from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from spots.models import Spot


class SpotPR10Tests(TestCase):
    def test_slug_and_get_absolute_url(self):
        spot = Spot.objects.create(number="B7", covered=False, daily_rate="300.00")
        self.assertTrue(spot.slug.startswith("mesto-b7"))
        self.assertEqual(spot.get_absolute_url(), reverse("spots:detail", kwargs={"slug": spot.slug}))
        response = self.client.get(spot.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "B7")

    def test_unknown_slug_returns_404(self):
        response = self.client.get(reverse("spots:detail", kwargs={"slug": "missing-slug"}))
        self.assertEqual(response.status_code, 404)

    def test_generated_field_is_expensive(self):
        spot = Spot.objects.create(number="B8", covered=False, daily_rate="300.00")
        spot.refresh_from_db()
        self.assertFalse(spot.is_expensive)
        spot.daily_rate = Decimal("600.00")
        spot.save()
        spot.refresh_from_db()
        self.assertTrue(spot.is_expensive)

    def test_context_processor_data(self):
        Spot.objects.create(number="B9", covered=False, daily_rate="300.00")
        Spot.objects.create(number="B10", covered=True, daily_rate="600.00")
        response = self.client.get(reverse("spots:list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["site_name"], "Parking Booking")
        self.assertEqual(response.context["spots_count"], 2)

    def test_sort_by_rate_desc(self):
        Spot.objects.create(number="B11", covered=False, daily_rate="300.00")
        Spot.objects.create(number="B12", covered=True, daily_rate="600.00")
        response = self.client.get(reverse("spots:list"), {"sort": "rate", "direction": "desc"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["spots"][0].daily_rate, Decimal("600.00"))