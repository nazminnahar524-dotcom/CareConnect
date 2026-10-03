from datetime import time

from django.core.management.base import BaseCommand

from pharmacies.models import Pharmacy


class Command(BaseCommand):
    help = "Seed sample CareConnect pharmacies into the database"

    def handle(self, *args, **kwargs):

        pharmacies = [
            {
                "name": "CarePlus Pharmacy",
                "license_number": "PH-DHK-001",
                "license_status": "Active",
                "address": "Dhanmondi, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Dhanmondi",
                "latitude": 23.7465,
                "longitude": 90.3760,
                "phone": "01700000001",
                "email": "careplus@example.com",
                "opening_time": time(8, 0),
                "closing_time": time(23, 0),
                "is_24_7": False,
                "emergency": True,
                "home_delivery": True,
                "online_order": True,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "MediCare Pharmacy",
                "license_number": "PH-DHK-002",
                "license_status": "Active",
                "address": "Mirpur, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Mirpur",
                "latitude": 23.8223,
                "longitude": 90.3654,
                "phone": "01700000002",
                "email": "medicare@example.com",
                "opening_time": time(9, 0),
                "closing_time": time(22, 0),
                "is_24_7": False,
                "emergency": False,
                "home_delivery": True,
                "online_order": True,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "HealthCare Pharmacy",
                "license_number": "PH-DHK-003",
                "license_status": "Active",
                "address": "Uttara, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Uttara",
                "latitude": 23.8759,
                "longitude": 90.3795,
                "phone": "01700000003",
                "email": "healthcare@example.com",
                "opening_time": None,
                "closing_time": None,
                "is_24_7": True,
                "emergency": True,
                "home_delivery": True,
                "online_order": True,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "LifeLine Pharmacy",
                "license_number": "PH-DHK-004",
                "license_status": "Active",
                "address": "Mohammadpur, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Mohammadpur",
                "latitude": 23.7662,
                "longitude": 90.3589,
                "phone": "01700000004",
                "email": "lifeline@example.com",
                "opening_time": time(8, 0),
                "closing_time": time(22, 0),
                "is_24_7": False,
                "emergency": False,
                "home_delivery": True,
                "online_order": False,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "City Pharmacy",
                "license_number": "PH-DHK-005",
                "license_status": "Active",
                "address": "Gulshan, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Gulshan",
                "latitude": 23.7925,
                "longitude": 90.4078,
                "phone": "01700000005",
                "email": "citypharmacy@example.com",
                "opening_time": time(9, 0),
                "closing_time": time(23, 0),
                "is_24_7": False,
                "emergency": True,
                "home_delivery": True,
                "online_order": True,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "Medix Pharmacy",
                "license_number": "PH-DHK-006",
                "license_status": "Active",
                "address": "Banani, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Banani",
                "latitude": 23.7937,
                "longitude": 90.4043,
                "phone": "01700000006",
                "email": "medix@example.com",
                "opening_time": time(8, 0),
                "closing_time": time(21, 0),
                "is_24_7": False,
                "emergency": False,
                "home_delivery": True,
                "online_order": True,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "Wellness Pharmacy",
                "license_number": "PH-DHK-007",
                "license_status": "Active",
                "address": "Bashundhara, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Bashundhara",
                "latitude": 23.8223,
                "longitude": 90.4250,
                "phone": "01700000007",
                "email": "wellness@example.com",
                "opening_time": time(9, 0),
                "closing_time": time(22, 0),
                "is_24_7": False,
                "emergency": False,
                "home_delivery": True,
                "online_order": True,
                "medicine_available": True,
                "verified": True,
            },
            {
                "name": "Trust Pharmacy",
                "license_number": "PH-DHK-008",
                "license_status": "Active",
                "address": "Farmgate, Dhaka",
                "division": "Dhaka",
                "district": "Dhaka",
                "area": "Farmgate",
                "latitude": 23.7579,
                "longitude": 90.3890,
                "phone": "01700000008",
                "email": "trust@example.com",
                "opening_time": time(8, 0),
                "closing_time": time(23, 0),
                "is_24_7": False,
                "emergency": True,
                "home_delivery": False,
                "online_order": False,
                "medicine_available": True,
                "verified": True,
            },
        ]

        created_count = 0
        updated_count = 0

        for data in pharmacies:
            pharmacy, created = Pharmacy.objects.update_or_create(
                license_number=data["license_number"],
                defaults=data
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{created_count} pharmacies created, "
                f"{updated_count} pharmacies updated."
            )
        )