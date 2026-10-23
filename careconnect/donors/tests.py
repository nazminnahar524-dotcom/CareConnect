from django.test import TestCase
from django.urls import reverse

from .models import Donor


class NearbyDonorAddressFilterTests(TestCase):
    def setUp(self):
        self.mirpur_donor = Donor.objects.create(
            full_name='Mirpur O Positive',
            gender='Female',
            blood_group='O+',
            phone_number='01700000001',
            district='Dhaka',
            upazila='Mirpur',
            area='Pallabi',
        )
        Donor.objects.create(
            full_name='Mirpur A Positive',
            gender='Male',
            blood_group='A+',
            phone_number='01700000002',
            district='Dhaka',
            upazila='Mirpur',
            area='Pallabi',
        )
        Donor.objects.create(
            full_name='Chattogram O Positive',
            gender='Male',
            blood_group='O+',
            phone_number='01700000003',
            district='Chattogram',
            upazila='Pahartali',
            area='Pahartali',
        )

    def test_filters_by_address_and_keeps_blood_group_filter(self):
        response = self.client.get(
            reverse('nearby_donors'),
            {'address': 'mirpur', 'blood_group': 'O+'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mirpur_donor.full_name)
        self.assertNotContains(response, 'Mirpur A Positive')
        self.assertNotContains(response, 'Chattogram O Positive')
        self.assertEqual(response.context['selected_address'], 'mirpur')
