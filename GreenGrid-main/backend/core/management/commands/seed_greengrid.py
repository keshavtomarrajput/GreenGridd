"""
Custom Django management command to seed GreenGrid database with realistic Indian-context data.
Run with: python manage.py seed_greengrid
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
import datetime
from decimal import Decimal

from core.models import (
    Role, UserAccount, Facility, Meter, TelemetryReading,
    Benchmark, UtilityProvider, UtilityBill, Recommendation,
    RenewableSystem, RenewableGenerationLog, DemandResponseEvent
)

class Command(BaseCommand):
    help = 'Seeds GreenGrid database with complete master and transaction test records.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🌱 Starting GreenGrid automated database seeding..."))

        # 1. Roles
        roles_data = [
            (1, 'Administrator', 'System wide access and governance'),
            (2, 'Facility Manager', 'Oversees energy budgets and retrofit approvals'),
            (3, 'Field Engineer', 'Hardware meter commissioning and maintenance'),
            (4, 'Energy Auditor', 'Conducts ISO 50001 compliance reviews')
        ]
        for rid, name, desc in roles_data:
            Role.objects.get_or_create(role_id=rid, defaults={'role_name': name, 'role_description': desc})
        self.stdout.write(self.style.SUCCESS("✓ Seeded Roles"))

        # 2. Users
        users_data = [
            (1, 'admin_greengrid', 'admin@greengrid.in', 'Rajesh K. Sharma', '+91-9811223344', 1),
            (2, 'mgr_arun_bengaluru', 'arun.nair@greengrid.in', 'Arun V. Nair', '+91-9845012345', 2),
            (3, 'mgr_priya_pune', 'priya.deshmukh@greengrid.in', 'Priya Deshmukh', '+91-9822098765', 2),
            (4, 'mgr_vikram_hyderabad', 'vikram.reddy@greengrid.in', 'Vikramaditya Reddy', '+91-9988776655', 2),
            (5, 'eng_sanjay_field', 'sanjay.patel@greengrid.in', 'Sanjay Patel', '+91-9711224466', 3),
            (6, 'eng_deepak_field', 'deepak.verma@greengrid.in', 'Deepak Verma', '+91-9899001122', 3),
            (7, 'auditor_ananya', 'ananya.sen@greengrid.in', 'Ananya Sengupta', '+91-9833445566', 4)
        ]
        for uid, uname, email, fname, phone, rid in users_data:
            role = Role.objects.get(role_id=rid)
            UserAccount.objects.get_or_create(
                user_id=uid,
                defaults={
                    'username': uname,
                    'email': email,
                    'password_hash': 'pbkdf2_sha256$600000$demo$placeholder',
                    'full_name': fname,
                    'phone_number': phone,
                    'role': role,
                    'is_active': True
                }
            )
        self.stdout.write(self.style.SUCCESS("✓ Seeded User Accounts"))

        # 3. Facilities
        manager_blr = UserAccount.objects.get(user_id=2)
        manager_pun = UserAccount.objects.get(user_id=3)
        manager_hyd = UserAccount.objects.get(user_id=4)

        fac_data = [
            (1, 'BLR-FAC-01', 'Manyata Tech Park Tower 7', 'IT Park', 'Outer Ring Road, Nagavara', 'Bengaluru', 'Karnataka', '560045', 250000, 2018, manager_blr, 142.5),
            (2, 'BLR-FAC-02', 'Electronic City Campus B', 'IT Park', 'Phase 1, Hosur Road', 'Bengaluru', 'Karnataka', '560100', 180000, 2016, manager_blr, 138.0),
            (3, 'PUN-FAC-01', 'Hinjawadi Infotech Zone 3', 'IT Park', 'Phase 2, Hinjawadi', 'Pune', 'Maharashtra', '411057', 310000, 2019, manager_pun, 155.0),
            (4, 'PUN-FAC-02', 'Chakan Auto Components Plant', 'Manufacturing Plant', 'MIDC Phase II', 'Pune', 'Maharashtra', '410501', 145000, 2015, manager_pun, 260.0),
            (5, 'HYD-FAC-01', 'HITEC City Cyber Gateways', 'Commercial Office', 'Madhapur', 'Hyderabad', 'Telangana', '500081', 220000, 2020, manager_hyd, 132.0),
            (6, 'HYD-FAC-02', 'Genome Valley BioPharma Lab', 'Manufacturing Plant', 'Shamirpet', 'Hyderabad', 'Telangana', '500078', 95000, 2021, manager_hyd, 310.0),
            (7, 'MUM-FAC-01', 'BKC Financial Center West', 'Commercial Office', 'Bandra Kurla Complex', 'Mumbai', 'Maharashtra', '400051', 340000, 2018, manager_pun, 175.0),
            (8, 'BLR-FAC-03', 'Whitefield Eco-Care Hospital', 'Hospital', 'ITPL Main Road', 'Bengaluru', 'Karnataka', '560066', 160000, 2020, manager_blr, 285.0)
        ]
        for fid, fcode, name, ftype, addr, city, state, pin, area, yr, mgr, base_epi in fac_data:
            Facility.objects.get_or_create(
                facility_id=fid,
                defaults={
                    'facility_code': fcode,
                    'name': name,
                    'facility_type': ftype,
                    'address': addr,
                    'city': city,
                    'state': state,
                    'pincode': pin,
                    'total_area_sqft': Decimal(str(area)),
                    'built_year': yr,
                    'manager': mgr,
                    'baseline_kwh_per_sqm': Decimal(str(base_epi))
                }
            )
        self.stdout.write(self.style.SUCCESS("✓ Seeded Facilities"))

        # 4. Benchmarks
        bench_data = [
            (1, 'IT Park', 'Moderate', 'BEE Commercial Buildings - Moderate Zone', 140, 200, 175, 150, 125, 100),
            (2, 'Commercial Office', 'Composite', 'BEE Office Buildings - Composite Zone', 160, 220, 190, 165, 135, 110),
            (3, 'Hospital', 'Warm and Humid', 'BEE Healthcare Star Rating Standard', 275, 380, 340, 300, 260, 220),
            (4, 'Manufacturing Plant', 'Hot and Dry', 'Industrial Energy Efficiency Guideline', 250, 350, 310, 270, 230, 190)
        ]
        for bid, ftype, czone, bname, epi, s1, s2, s3, s4, s5 in bench_data:
            Benchmark.objects.get_or_create(
                benchmark_id=bid,
                defaults={
                    'facility_type': ftype,
                    'climate_zone': czone,
                    'benchmark_name': bname,
                    'standard_epi_kwh_sqm_yr': Decimal(str(epi)),
                    'bee_star_1_max': Decimal(str(s1)),
                    'bee_star_2_max': Decimal(str(s2)),
                    'bee_star_3_max': Decimal(str(s3)),
                    'bee_star_4_max': Decimal(str(s4)),
                    'bee_star_5_max': Decimal(str(s5))
                }
            )
        self.stdout.write(self.style.SUCCESS("✓ Seeded BEE Benchmarks"))

        # 5. Utility Providers
        providers_data = [
            (1, 'Bangalore Electricity Supply Company (BESCOM)', 'Karnataka', 'HT-2(a) Commercial', '1912'),
            (2, 'Maharashtra State Electricity Distribution Co (MSEDCL)', 'Maharashtra', 'HT-I Industrial & Commercial', '1800-233-3435'),
            (3, 'Telangana Southern Power Distribution Co (TSSPDCL)', 'Telangana', 'HT Category-II', '1912')
        ]
        for pid, pname, pstate, tcode, care in providers_data:
            UtilityProvider.objects.get_or_create(
                provider_id=pid,
                defaults={'provider_name': pname, 'state': pstate, 'tariff_code': tcode, 'customer_care_no': care}
            )
        self.stdout.write(self.style.SUCCESS("✓ Seeded Utility Providers"))

        # 6. Meters & Telemetry
        fac_1 = Facility.objects.get(facility_id=1)
        meters_data = [
            (1, 'SCH-MTR-BLR-001', fac_1, 'Manyata Main Grid Incomer Feeder', 'Main Incomer', 'Schneider Electric', 'ION9000', '192.168.10.21', 1),
            (2, 'SCH-MTR-BLR-002', fac_1, 'Manyata Central Chiller Plant 1', 'HVAC Feeder', 'Schneider Electric', 'PM8000', '192.168.10.22', 2),
            (3, 'ABB-MTR-BLR-003', fac_1, 'Manyata Server Room UPS Bus A', 'UPS & Data Center', 'ABB', 'M4M 30', '192.168.10.23', 3),
            (4, 'SCH-MTR-BLR-004', fac_1, 'Manyata Rooftop 250kW Solar Feeder', 'Solar Inverter Feed', 'Schneider Electric', 'PM5560', '192.168.10.24', 4)
        ]
        for mid, sno, fac, mname, mtype, mfg, mdl, ip, slave in meters_data:
            meter, _ = Meter.objects.get_or_create(
                meter_id=mid,
                defaults={
                    'meter_serial_no': sno,
                    'facility': fac,
                    'meter_name': mname,
                    'meter_type': mtype,
                    'manufacturer': mfg,
                    'model': mdl,
                    'installation_date': datetime.date(2023, 1, 15),
                    'status': 'Active',
                    'ip_address': ip,
                    'modbus_slave_id': slave
                }
            )
            if mid == 1 and not TelemetryReading.objects.filter(meter=meter).exists():
                now = timezone.now()
                for h in range(12):
                    t = now - datetime.timedelta(hours=(12 - h))
                    TelemetryReading.objects.create(
                        meter=meter,
                        reading_timestamp=t,
                        active_power_kw=Decimal(str(600 + (h * 45))),
                        reactive_power_kvar=Decimal(str(150 + (h * 12))),
                        voltage_v=Decimal('415.2'),
                        current_a=Decimal(str(850 + (h * 50))),
                        power_factor=Decimal('0.956'),
                        frequency_hz=Decimal('50.01'),
                        cumulative_energy_kwh=Decimal(str(1280000 + (h * 650)))
                    )
        self.stdout.write(self.style.SUCCESS("✓ Seeded Smart Meters & Telemetry"))

        # 7. Utility Bills
        p_bescom = UtilityProvider.objects.get(provider_id=1)
        UtilityBill.objects.get_or_create(
            bill_id=1,
            defaults={
                'facility': fac_1,
                'provider': p_bescom,
                'consumer_account_no': 'BES-CA-9041284',
                'bill_number': 'BESCOM-2026-OCT-0941',
                'billing_month': 10,
                'billing_year': 2026,
                'units_consumed_kwh': Decimal('482500.00'),
                'peak_units_kwh': Decimal('168000.00'),
                'off_peak_units_kwh': Decimal('314500.00'),
                'billed_amount_inr': Decimal('4101250.00'),
                'tariff_rate_inr_kwh': Decimal('8.50'),
                'due_date': datetime.date(2026, 11, 15),
                'payment_status': 'Paid',
                'verified_by': manager_blr
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ Seeded Utility Bills"))

        # 8. Energy Efficiency Recommendations
        recs = [
            (1, fac_1, 'VFD Retrofit on Central Chiller Condenser Pumps', 'HVAC Optimization', 'Install Variable Frequency Drives to dynamically modulate pump speed.', 850000, 100000, 1200000, 16.9, 'Approved', 'High'),
            (2, fac_1, 'Automatic Capacitor Bank PF Correction', 'Power Factor Correction', 'Deploy 150 kVAR switched APFC capacitor banks to raise plant average PF to 0.99.', 420000, 45000, 380000, 10.8, 'Implemented', 'Critical')
        ]
        for rid, fac, title, cat, desc, sav_inr, sav_kwh, cost, pb, stat, pri in recs:
            Recommendation.objects.get_or_create(
                recommendation_id=rid,
                defaults={
                    'facility': fac,
                    'title': title,
                    'category': cat,
                    'description': desc,
                    'estimated_annual_savings_inr': Decimal(str(sav_inr)),
                    'estimated_kwh_savings': Decimal(str(sav_kwh)),
                    'implementation_cost_inr': Decimal(str(cost)),
                    'payback_period_months': Decimal(str(pb)),
                    'status': stat,
                    'priority': pri
                }
            )
        self.stdout.write(self.style.SUCCESS("✓ Seeded Energy Recommendations"))

        # 9. Renewables & Smart Grid
        RenewableSystem.objects.get_or_create(
            system_id=1,
            defaults={
                'facility': fac_1,
                'system_type': 'Rooftop Solar PV',
                'capacity_kw': Decimal('250.00'),
                'installation_date': datetime.date(2023, 2, 15),
                'inverter_model': 'SMA Sunny Tripower CORE2 110kW',
                'tilt_angle': Decimal('15.0'),
                'azimuth_angle': Decimal('180.0'),
                'status': 'Generating'
            }
        )
        RenewableSystem.objects.get_or_create(
            system_id=2,
            defaults={
                'facility': fac_1,
                'system_type': 'Battery Storage (BESS)',
                'capacity_kw': Decimal('150.00'),
                'installation_date': datetime.date(2023, 4, 20),
                'inverter_model': 'Tesla Megapack Commercial Li-Ion',
                'status': 'Generating'
            }
        )
        self.stdout.write(self.style.SUCCESS("✓ Seeded Renewable Systems"))

        self.stdout.write(self.style.SUCCESS("🎉 GreenGrid Database seeding completed successfully!"))
