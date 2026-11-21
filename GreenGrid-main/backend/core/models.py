"""
GreenGrid Django ORM Models
3NF Normalized Relational Schema supporting all 8 Energy Management Modules
"""

from django.db import models
from django.utils import timezone

# ----------------------------------------------------------------------------
# Module 8: Role-Based Access Control & User Management
# ----------------------------------------------------------------------------
class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=50, unique=True)
    role_description = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.role_name

    class Meta:
        db_table = 'roles'


class UserAccount(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, related_name='users')
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.username}) - {self.role.role_name}"

    class Meta:
        db_table = 'users'


# ----------------------------------------------------------------------------
# Module 1: Facility Infrastructure & Smart Meters
# ----------------------------------------------------------------------------
class Facility(models.Model):
    FACILITY_TYPES = [
        ('Commercial Office', 'Commercial Office'),
        ('IT Park', 'IT Park'),
        ('Manufacturing Plant', 'Manufacturing Plant'),
        ('Hospital', 'Hospital'),
        ('Educational Campus', 'Educational Campus'),
        ('Retail Mall', 'Retail Mall')
    ]

    facility_id = models.AutoField(primary_key=True)
    facility_code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    facility_type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    total_area_sqft = models.DecimalField(max_digits=12, decimal_places=2)
    built_year = models.IntegerField()
    manager = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_facilities')
    baseline_kwh_per_sqm = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.city}) [{self.facility_code}]"

    class Meta:
        db_table = 'facilities'


class Meter(models.Model):
    METER_TYPES = [
        ('Main Incomer', 'Main Incomer'),
        ('HVAC Feeder', 'HVAC Feeder'),
        ('Lighting', 'Lighting'),
        ('UPS & Data Center', 'UPS & Data Center'),
        ('Industrial Machinery', 'Industrial Machinery'),
        ('Solar Inverter Feed', 'Solar Inverter Feed')
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
        ('Offline', 'Offline')
    ]

    meter_id = models.AutoField(primary_key=True)
    meter_serial_no = models.CharField(max_length=60, unique=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='meters')
    meter_name = models.CharField(max_length=150)
    meter_type = models.CharField(max_length=50, choices=METER_TYPES)
    manufacturer = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    installation_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    ip_address = models.CharField(max_length=45, null=True, blank=True)
    modbus_slave_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.meter_name} ({self.meter_serial_no}) - {self.facility.name}"

    class Meta:
        db_table = 'meters'


class TelemetryReading(models.Model):
    reading_id = models.BigAutoField(primary_key=True)
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='readings')
    reading_timestamp = models.DateTimeField()
    active_power_kw = models.DecimalField(max_digits=10, decimal_places=3)
    reactive_power_kvar = models.DecimalField(max_digits=10, decimal_places=3)
    voltage_v = models.DecimalField(max_digits=6, decimal_places=2)
    current_a = models.DecimalField(max_digits=8, decimal_places=2)
    power_factor = models.DecimalField(max_digits=4, decimal_places=3)
    frequency_hz = models.DecimalField(max_digits=5, decimal_places=2, default=50.00)
    cumulative_energy_kwh = models.DecimalField(max_digits=14, decimal_places=3)
    recorded_by = models.CharField(max_length=50, default='MODBUS_GATEWAY')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Mtr {self.meter_id} @ {self.reading_timestamp}: {self.active_power_kw} kW (PF: {self.power_factor})"

    class Meta:
        db_table = 'telemetry_readings'
        indexes = [
            models.Index(fields=['reading_timestamp']),
            models.Index(fields=['meter', 'reading_timestamp']),
        ]


# ----------------------------------------------------------------------------
# Module 4: Energy Benchmarking (BEE Star Ratings & Standards)
# ----------------------------------------------------------------------------
class Benchmark(models.Model):
    CLIMATE_ZONES = [
        ('Warm and Humid', 'Warm and Humid'),
        ('Composite', 'Composite'),
        ('Hot and Dry', 'Hot and Dry'),
        ('Moderate', 'Moderate'),
        ('Cold', 'Cold')
    ]

    benchmark_id = models.AutoField(primary_key=True)
    facility_type = models.CharField(max_length=100)
    climate_zone = models.CharField(max_length=50, choices=CLIMATE_ZONES)
    benchmark_name = models.CharField(max_length=150)
    standard_epi_kwh_sqm_yr = models.DecimalField(max_digits=8, decimal_places=2)
    bee_star_1_max = models.DecimalField(max_digits=8, decimal_places=2)
    bee_star_2_max = models.DecimalField(max_digits=8, decimal_places=2)
    bee_star_3_max = models.DecimalField(max_digits=8, decimal_places=2)
    bee_star_4_max = models.DecimalField(max_digits=8, decimal_places=2)
    bee_star_5_max = models.DecimalField(max_digits=8, decimal_places=2)
    reference_standard = models.CharField(max_length=100, default='BEE Energy Conservation Code')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.benchmark_name} ({self.climate_zone})"

    class Meta:
        db_table = 'benchmarks'


# ----------------------------------------------------------------------------
# Module 5: Utility Bill Management (Discom HT Tariffs in INR)
# ----------------------------------------------------------------------------
class UtilityProvider(models.Model):
    DISCOM_TYPES = [
        ('State Discom', 'State Discom'),
        ('Private Discom', 'Private Discom'),
        ('Municipal Body', 'Municipal Body')
    ]

    provider_id = models.AutoField(primary_key=True)
    provider_name = models.CharField(max_length=150, unique=True)
    state = models.CharField(max_length=100)
    tariff_code = models.CharField(max_length=50)
    customer_care_no = models.CharField(max_length=20, null=True, blank=True)
    discom_type = models.CharField(max_length=50, choices=DISCOM_TYPES, default='State Discom')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.provider_name} ({self.state})"

    class Meta:
        db_table = 'utility_providers'


class UtilityBill(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Paid', 'Paid'),
        ('Disputed', 'Disputed')
    ]

    bill_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.RESTRICT, related_name='bills')
    provider = models.ForeignKey(UtilityProvider, on_delete=models.RESTRICT, related_name='bills')
    consumer_account_no = models.CharField(max_length=50)
    bill_number = models.CharField(max_length=80, unique=True)
    billing_month = models.IntegerField()
    billing_year = models.IntegerField()
    units_consumed_kwh = models.DecimalField(max_digits=12, decimal_places=2)
    peak_units_kwh = models.DecimalField(max_digits=12, decimal_places=2)
    off_peak_units_kwh = models.DecimalField(max_digits=12, decimal_places=2)
    billed_amount_inr = models.DecimalField(max_digits=12, decimal_places=2)
    tariff_rate_inr_kwh = models.DecimalField(max_digits=6, decimal_places=2)
    penalty_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    due_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    verified_by = models.ForeignKey(UserAccount, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_bills')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Bill {self.bill_number} - {self.facility.name} (₹{self.billed_amount_inr})"

    class Meta:
        db_table = 'utility_bills'


# ----------------------------------------------------------------------------
# Module 6: Energy Efficiency Recommendations
# ----------------------------------------------------------------------------
class Recommendation(models.Model):
    CATEGORIES = [
        ('HVAC Optimization', 'HVAC Optimization'),
        ('Lighting Retrofit', 'Lighting Retrofit'),
        ('Peak Shaving', 'Peak Shaving'),
        ('Power Factor Correction', 'Power Factor Correction'),
        ('Solar Expansion', 'Solar Expansion'),
        ('Behavioral', 'Behavioral')
    ]
    STATUS_CHOICES = [
        ('Proposed', 'Proposed'),
        ('Under Review', 'Under Review'),
        ('Approved', 'Approved'),
        ('Implemented', 'Implemented'),
        ('Rejected', 'Rejected')
    ]
    PRIORITIES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
        ('Critical', 'Critical')
    ]

    recommendation_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='recommendations')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORIES)
    description = models.TextField()
    estimated_annual_savings_inr = models.DecimalField(max_digits=12, decimal_places=2)
    estimated_kwh_savings = models.DecimalField(max_digits=12, decimal_places=2)
    implementation_cost_inr = models.DecimalField(max_digits=12, decimal_places=2)
    payback_period_months = models.DecimalField(max_digits=5, decimal_places=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Proposed')
    priority = models.CharField(max_length=20, choices=PRIORITIES, default='Medium')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - ₹{self.estimated_annual_savings_inr}/yr ({self.status})"

    class Meta:
        db_table = 'recommendations'


# ----------------------------------------------------------------------------
# Module 7: Renewable Energy & Smart Grid Integration
# ----------------------------------------------------------------------------
class RenewableSystem(models.Model):
    SYSTEM_TYPES = [
        ('Rooftop Solar PV', 'Rooftop Solar PV'),
        ('Wind Turbine', 'Wind Turbine'),
        ('Battery Storage (BESS)', 'Battery Storage (BESS)'),
        ('Hybrid Solar-Wind', 'Hybrid Solar-Wind')
    ]
    STATUS_CHOICES = [
        ('Generating', 'Generating'),
        ('Standby', 'Standby'),
        ('Maintenance', 'Maintenance'),
        ('Fault', 'Fault')
    ]

    system_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='renewable_systems')
    system_type = models.CharField(max_length=50, choices=SYSTEM_TYPES)
    capacity_kw = models.DecimalField(max_digits=10, decimal_places=2)
    installation_date = models.DateField()
    inverter_model = models.CharField(max_length=100)
    tilt_angle = models.DecimalField(max_digits=4, decimal_places=1, default=15.0)
    azimuth_angle = models.DecimalField(max_digits=5, decimal_places=1, default=180.0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Generating')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.system_type} ({self.capacity_kw} kW) - {self.facility.name}"

    class Meta:
        db_table = 'renewable_systems'


class RenewableGenerationLog(models.Model):
    log_id = models.BigAutoField(primary_key=True)
    system = models.ForeignKey(RenewableSystem, on_delete=models.CASCADE, related_name='generation_logs')
    log_timestamp = models.DateTimeField()
    generation_kwh = models.DecimalField(max_digits=10, decimal_places=2)
    battery_charge_kwh = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    battery_discharge_kwh = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grid_export_kwh = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grid_import_kwh = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    battery_soc_percent = models.DecimalField(max_digits=5, decimal_places=2, default=80.00)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.system.system_type} @ {self.log_timestamp}: {self.generation_kwh} kWh (SOC: {self.battery_soc_percent}%)"

    class Meta:
        db_table = 'renewable_generation_logs'


class DemandResponseEvent(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled')
    ]

    event_id = models.AutoField(primary_key=True)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='dr_events')
    event_title = models.CharField(max_length=150)
    target_shed_kw = models.DecimalField(max_digits=10, decimal_places=2)
    actual_shed_kw = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    incentive_earned_inr = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.event_title} ({self.status}) - Target: {self.target_shed_kw} kW"

    class Meta:
        db_table = 'demand_response_events'


# ----------------------------------------------------------------------------
# Legacy Models (Maintained for backward schema compatibility)
# ----------------------------------------------------------------------------
class Device(models.Model):
    DEVICE_TYPES = [
        ('AC', 'Air Conditioner'),
        ('FAN', 'Fan'),
        ('LIGHT', 'Light'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=20, choices=DEVICE_TYPES)
    power_rating = models.FloatField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class EnergyUsage(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='energy_records')
    energy_consumed = models.DecimalField(max_digits=10, decimal_places=3)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.device.name} - {self.energy_consumed} kWh"


class Bill(models.Model):
    total_units = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Bill - Rs. {self.total_amount}"
