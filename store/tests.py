from django.test import TestCase
from django.urls import reverse
from .models import Album, Artist, Contact, Booking

# Create your tests here.

# Index page should return 200


class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
# Detail page should return 200 if exists, 404 if not


class DetailPageTestCase(TestCase):

    def test_detail_page_returns_200(self):
        impossible = Album.objects.create(title="Transmission impossible")
        album_id = impossible.id
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        impossible = Album.objects.create(title="Transmission impossible")
        album_id = impossible.id + 1
        response = self.client.get(reverse('store:detail', args=(album_id,)))
        self.assertEqual(response.status_code, 404)

        # Booking
        # test new booking
        # test booking belongs to contact
        # test booking belongs to album
