from io import BytesIO
import tempfile

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test import override_settings
from django.urls import reverse
from PIL import Image

from .admin import DonorAdmin
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
        Donor.objects.create(
            full_name='Unavailable Donor',
            gender='Male',
            blood_group='A+',
            phone_number='01700000004',
            district='Dhaka',
            upazila='Dhanmondi',
            area='Dhanmondi',
            is_available=False,
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
        self.assertNotContains(response, 'Unavailable Donor')
        self.assertContains(response, '1 Donors Found')
        self.assertContains(response, '0.0 km away')
        self.assertEqual(response.context['selected_address'], 'mirpur')
        self.assertEqual(response.context['available_donors_count'], 3)

    def test_default_nearby_page_shows_available_donors_outside_local_radius(self):
        distant_donor = Donor.objects.create(
            full_name='Distant Registered Donor',
            gender='Male',
            blood_group='AB+',
            phone_number='01700000005',
            district='Sylhet',
            upazila='Sylhet Sadar',
            area='Sylhet',
            latitude=24.8949,
            longitude=91.8687,
        )

        response = self.client.get(reverse('nearby_donors'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, distant_donor.full_name)
        self.assertEqual(response.context['total_donors'], 4)
        self.assertEqual(response.context['radius'], 20050.0)

        limited_response = self.client.get(
            reverse('nearby_donors'),
            {'radius': '10'},
        )
        self.assertNotContains(limited_response, distant_donor.full_name)

    def test_inactive_donor_profile_is_not_publicly_accessible(self):
        inactive_donor = Donor.objects.get(full_name='Unavailable Donor')

        response = self.client.get(
            reverse('donor_detail', args=[inactive_donor.pk])
        )

        self.assertEqual(response.status_code, 404)

    def test_admin_can_toggle_donor_availability_from_list(self):
        donor = self.mirpur_donor
        admin_user = get_user_model().objects.create_superuser(
            username='donor-admin',
            email='admin@example.com',
            password='Secure-test-password-123!',
        )
        self.client.force_login(admin_user)

        self.assertIn('is_available', DonorAdmin.list_editable)
        changelist_url = reverse('admin:donors_donor_changelist')
        response = self.client.get(changelist_url)
        self.assertEqual(response.status_code, 200)

        rows = list(response.context['cl'].result_list)
        def post_availability(is_available):
            data = {
                'form-TOTAL_FORMS': str(len(rows)),
                'form-INITIAL_FORMS': str(len(rows)),
                'form-MIN_NUM_FORMS': '0',
                'form-MAX_NUM_FORMS': '1000',
                '_save': 'Save',
            }
            for index, row in enumerate(rows):
                data[f'form-{index}-id'] = str(row.pk)
                if row.pk != donor.pk or is_available:
                    data[f'form-{index}-is_available'] = 'on'
            return self.client.post(changelist_url, data)

        response = post_availability(False)
        self.assertEqual(response.status_code, 302)
        donor.refresh_from_db()
        self.assertFalse(donor.is_available)

        response = post_availability(True)
        self.assertEqual(response.status_code, 302)
        donor.refresh_from_db()
        self.assertTrue(donor.is_available)


class DonorRegistrationTests(TestCase):
    def setUp(self):
        self.registration_url = reverse('register_donor')
        self.valid_data = {
            'full_name': 'New Blood Donor',
            'blood_group': 'B+',
            'gender': 'Female',
            'age': '29',
            'district': 'Dhaka',
            'upazila': 'Mirpur',
            'area': 'Pallabi',
            'phone_number': '01712345678',
            'whatsapp_number': '01712345678',
            'email': 'donor@example.com',
            'occupation': 'Teacher',
            'languages': 'Bangla',
            'about_me': 'Ready to donate.',
            'is_available': 'on',
        }

    def test_address_field_does_not_suggest_a_default_location(self):
        response = self.client.get(self.registration_url)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Dhanmondi, Dhaka')
        self.assertContains(response, 'Enter your area or full address')

    def test_valid_registration_creates_donor_and_redirects(self):
        response = self.client.post(self.registration_url, self.valid_data)

        self.assertRedirects(response, reverse('nearby_donors'))
        donor = Donor.objects.get(full_name='New Blood Donor')
        self.assertEqual(donor.blood_group, 'B+')
        self.assertTrue(donor.is_available)
        nearby_response = self.client.get(reverse('nearby_donors'))
        self.assertContains(nearby_response, donor.full_name)
        self.assertContains(nearby_response, 'No profile photo')
        detail_response = self.client.get(
            reverse('donor_detail', args=[donor.pk])
        )
        self.assertContains(detail_response, 'No profile photo')

    def test_registration_accepts_optional_photo_and_shows_it_on_pages(self):
        image_buffer = BytesIO()
        Image.new('RGB', (2, 2), color='green').save(image_buffer, format='PNG')
        image_buffer.seek(0)
        photo = SimpleUploadedFile(
            'donor.png',
            image_buffer.read(),
            content_type='image/png',
        )

        with tempfile.TemporaryDirectory() as media_dir:
            with override_settings(MEDIA_ROOT=media_dir):
                response = self.client.post(
                    self.registration_url,
                    {**self.valid_data, 'profile_photo': photo},
                )

                self.assertRedirects(response, reverse('nearby_donors'))
                donor = Donor.objects.get(full_name='New Blood Donor')
                self.assertTrue(donor.profile_photo)
                self.assertTrue(donor.profile_photo.storage.exists(donor.profile_photo.name))

                nearby_response = self.client.get(reverse('nearby_donors'))
                self.assertContains(nearby_response, donor.profile_photo.url)
                self.assertContains(nearby_response, "New Blood Donor's profile photo")

                detail_response = self.client.get(
                    reverse('donor_detail', args=[donor.pk])
                )
                self.assertContains(detail_response, donor.profile_photo.url)
                self.assertContains(detail_response, "New Blood Donor's profile photo")

    def test_invalid_registration_displays_validation_errors(self):
        invalid_data = {**self.valid_data, 'district': ''}

        response = self.client.post(self.registration_url, invalid_data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the following errors:')
        self.assertContains(response, 'District')
        self.assertEqual(Donor.objects.count(), 0)

    def test_logged_in_user_registration_adds_another_donor_profile(self):
        user = get_user_model().objects.create_user(
            username='existing-donor',
            password='Secure-test-password-123!',
        )
        existing_donor = Donor.objects.create(
            user=user,
            full_name='Old Donor Name',
            gender='Male',
            blood_group='O+',
            phone_number='01700000000',
            district='Dhaka',
            area='Dhanmondi',
        )
        self.client.force_login(user)

        response = self.client.post(self.registration_url, self.valid_data)

        self.assertRedirects(response, reverse('nearby_donors'))
        existing_donor.refresh_from_db()
        self.assertEqual(existing_donor.full_name, 'Old Donor Name')
        new_donor = Donor.objects.get(full_name='New Blood Donor')
        self.assertIsNone(new_donor.user)
        self.assertEqual(Donor.objects.filter(user=user).count(), 1)
        nearby_response = self.client.get(reverse('nearby_donors'))
        self.assertContains(nearby_response, 'New Blood Donor')
        self.assertContains(nearby_response, '2 Donors Found')
        self.assertEqual(nearby_response.context['available_donors_count'], 2)

        detail_response = self.client.get(
            reverse('donor_detail', args=[new_donor.pk])
        )
        self.assertEqual(detail_response.status_code, 200)
