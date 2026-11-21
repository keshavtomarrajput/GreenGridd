"""
Django Admin Registration for GreenGrid
Registers all 8 energy management modules & legacy models.
"""

from django.contrib import admin
from .models import (
    Role, UserAccount, Facility, Meter, TelemetryReading,
    Benchmark, UtilityProvider, UtilityBill, Recommendation,
    RenewableSystem, RenewableGenerationLog, DemandResponseEvent,
    Device, EnergyUsage, Bill
)

# ---------------- Module 8: RBAC ----------------
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name', 'created_at')

@admin.register(UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'email', 'full_name', 'role', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    list_filter = ('role', 'is_active')

# ---------------- Module 1: Facilities & Meters ----------------
@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_code', 'name', 'facility_type', 'city', 'state', 'total_area_sqft', 'manager')
    search_fields = ('name', 'facility_code', 'city')
    list_filter = ('facility_type', 'state')

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ('meter_serial_no', 'meter_name', 'facility', 'meter_type', 'status', 'ip_address')
    list_filter = ('meter_type', 'status', 'facility')

@admin.register(TelemetryReading)
class TelemetryReadingAdmin(admin.ModelAdmin):
    list_display = ('reading_id', 'meter', 'reading_timestamp', 'active_power_kw', 'power_factor', 'frequency_hz')
    list_filter = ('meter__meter_type', 'reading_timestamp')

# ---------------- Module 4: Benchmarks ----------------
@admin.register(Benchmark)
class BenchmarkAdmin(admin.ModelAdmin):
    list_display = ('benchmark_name', 'facility_type', 'climate_zone', 'standard_epi_kwh_sqm_yr')

# ---------------- Module 5: Utility Bills ----------------
@admin.register(UtilityProvider)
class UtilityProviderAdmin(admin.ModelAdmin):
    list_display = ('provider_name', 'state', 'tariff_code', 'discom_type')

@admin.register(UtilityBill)
class UtilityBillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'facility', 'provider', 'billing_month', 'billing_year', 'billed_amount_inr', 'payment_status')
    list_filter = ('payment_status', 'billing_year')

# ---------------- Module 6: Recommendations ----------------
@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('title', 'facility', 'category', 'estimated_annual_savings_inr', 'payback_period_months', 'status', 'priority')
    list_filter = ('category', 'status', 'priority')

# ---------------- Module 7: Renewables & Smart Grid ----------------
@admin.register(RenewableSystem)
class RenewableSystemAdmin(admin.ModelAdmin):
    list_display = ('system_type', 'facility', 'capacity_kw', 'status')

@admin.register(RenewableGenerationLog)
class RenewableGenerationLogAdmin(admin.ModelAdmin):
    list_display = ('system', 'log_timestamp', 'generation_kwh', 'battery_soc_percent')

@admin.register(DemandResponseEvent)
class DemandResponseEventAdmin(admin.ModelAdmin):
    list_display = ('event_title', 'facility', 'target_shed_kw', 'actual_shed_kw', 'status')

# ---------------- Legacy Models ----------------
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'device_type', 'power_rating', 'is_active')

@admin.register(EnergyUsage)
class EnergyUsageAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'energy_consumed', 'recorded_at')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_units', 'rate_per_unit', 'total_amount', 'bill_date')
