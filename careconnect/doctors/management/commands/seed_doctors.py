from django.core.management.base import BaseCommand
from doctors.models import Doctor

class Command(BaseCommand):
    help = 'Seeds prominent specialist doctors into the database'

    def handle(self, *args, **kwargs):
        doctors_data = [
            ("Prof. Dr. ABM Abdullah", "MBBS, FCPS, MRCP", "Medicine Specialist", "Bangabandhu Sheikh Mujib Medical University", 1200),
            ("Prof. Dr. Syed Atiqul Haq", "MBBS, MD, FRCP", "Rheumatology Specialist", "Birdem General Hospital", 1500),
            ("Prof. Dr. Quazi Deen Mohammad", "MBBS, MD, FCPS", "Neurology", "National Institute of Neurosciences", 1800),
            ("Prof. Dr. Harun-or-Rashid", "MBBS, FCPS, FRCP", "Nephrology", "Kidney Foundation Hospital", 1400),
            ("Prof. Dr. Abdul Wadud Chowdhury", "MBBS, FCPS", "Cardiology", "Dhaka Medical College", 1500),
            ("Dr. Zakiur Rahman", "MBBS, FCPS", "Cardiology", "Square Hospital", 1200),
            ("Dr. Farhana Dewan", "MBBS, FCPS", "Gynecology & Obstetrics", "Monowara Hospital", 1100),
            ("Prof. Dr. Shamim Ahmed", "MBBS, FCPS", "Pediatrics", "Bangladesh Specialized Hospital", 1000),
            ("Dr. Monjur Morshed", "MBBS, MD", "Dermatology", "Popular Diagnostic Centre", 1000),
            ("Prof. Dr. M. A. Wahab", "MBBS, FCPS", "Endocrinology & Diabetes", "BIRDEM", 1300),
        ]

        for doc in doctors_data:
            Doctor.objects.get_or_create(
                name=doc[0],
                defaults={
                    'qualification': doc[1],
                    'specialty': doc[2],
                    'hospital_name': doc[3],
                    'consultation_fee': doc[4],
                    'available_days': "Sat, Mon, Wed",
                    'visiting_hours': "5:00 PM - 8:00 PM",
                    'phone': "01700000000"
                }
            )
        self.stdout.write(self.style.SUCCESS('Successfully seeded sample doctors!'))