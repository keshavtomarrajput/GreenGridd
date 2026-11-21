"""
GreenGrid Django REST Framework Views & Web Controllers
"""

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum, Avg, Max, Min, Count
from django.utils import timezone
import datetime
from decimal import Decimal

from .models import (
    Role, UserAccount, Facility, Meter, TelemetryReading,
    Benchmark, UtilityProvider, UtilityBill, Recommendation,
    RenewableSystem, RenewableGenerationLog, DemandResponseEvent
)
from .serializers import (
    RoleSerializer, UserAccountSerializer, FacilitySerializer,
    MeterSerializer, TelemetryReadingSerializer, BenchmarkSerializer,
    UtilityProviderSerializer, UtilityBillSerializer, RecommendationSerializer,
    RenewableSystemSerializer, RenewableGenerationLogSerializer,
    DemandResponseEventSerializer
)

# ----------------- WEB DASHBOARD VIEW -----------------
def web_dashboard(request):
    """Renders the comprehensive EMIS web interface."""
    return render(request, 'index.html')

def api_root_view(request):
    """Returns REST API directory metadata."""
    return JsonResponse({
        "platform": "GreenGrid: Smart Energy Management for Tomorrow's Needs",
        "course": "FSD Python (P02)",
        "version": "1.0.0",
        "endpoints": {
            "web_dashboard": "/",
            "authentication": "/api/auth/",
            "facilities": "/api/facilities/",
            "meters": "/api/meters/",
            "telemetry": "/api/telemetry/",
            "analytics": "/api/analytics/",
            "benchmarks": "/api/benchmarks/",
            "bills": "/api/bills/",
            "recommendations": "/api/recommendations/",
            "renewables": "/api/renewables/",
            "demand_response": "/api/demand-response/",
            "users": "/api/users/"
        }
    })

# ============================================================================
# MODULE 8: User Management & Access Control
# ============================================================================
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('role_id')
    serializer_class = RoleSerializer

class UserAccountViewSet(viewsets.ModelViewSet):
    queryset = UserAccount.objects.select_related('role').all().order_by('user_id')
    serializer_class = UserAccountSerializer

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        user = UserAccount.objects.filter(username=username, is_active=True).first()
        if user:
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            return Response({
                "status": "success",
                "message": "Authentication successful",
                "user": {
                    "user_id": user.user_id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role.role_name
                },
                "token": f"greengrid_token_{user.username}_{user.user_id}"
            })
        return Response({"status": "error", "message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ============================================================================
# MODULE 1: Data Acquisition & Facilities
# ============================================================================
class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.select_related('manager').all().order_by('facility_id')
    serializer_class = FacilitySerializer

class MeterViewSet(viewsets.ModelViewSet):
    queryset = Meter.objects.select_related('facility').all().order_by('meter_id')
    serializer_class = MeterSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        facility_id = self.request.query_params.get('facility_id')
        status_filter = self.request.query_params.get('status')
        if facility_id:
            qs = qs.filter(facility_id=facility_id)
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

class TelemetryReadingViewSet(viewsets.ModelViewSet):
    queryset = TelemetryReading.objects.select_related('meter').order_by('-reading_timestamp')
    serializer_class = TelemetryReadingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        meter_id = self.request.query_params.get('meter_id')
        if meter_id:
            qs = qs.filter(meter_id=meter_id)
        return qs[:100]

class DataIngestAPIView(APIView):
    """Ingests real-time Modbus/BMS hardware telemetry packets."""
    def post(self, request):
        data = request.data
        meter_id = data.get('meter_id')
        meter = Meter.objects.filter(meter_id=meter_id).first()
        if not meter:
            return Response({"error": "Meter not found"}, status=status.HTTP_404_NOT_FOUND)

        active_power = Decimal(str(data.get('active_power_kw', 0.0)))
        voltage = Decimal(str(data.get('voltage_v', 415.0)))
        current = Decimal(str(data.get('current_a', 0.0)))
        power_factor = Decimal(str(data.get('power_factor', 0.95)))
        reactive_power = Decimal(str(data.get('reactive_power_kvar', 0.0)))
        cum_kwh = Decimal(str(data.get('cumulative_energy_kwh', 0.0)))

        reading = TelemetryReading.objects.create(
            meter=meter,
            reading_timestamp=data.get('reading_timestamp', timezone.now()),
            active_power_kw=active_power,
            reactive_power_kvar=reactive_power,
            voltage_v=voltage,
            current_a=current,
            power_factor=power_factor,
            frequency_hz=data.get('frequency_hz', 50.00),
            cumulative_energy_kwh=cum_kwh,
            recorded_by=data.get('recorded_by', 'MODBUS_GATEWAY')
        )

        if power_factor < Decimal('0.90'):
            meter.status = 'Warning'
            meter.save(update_fields=['status'])

        return Response({
            "status": "success",
            "message": "Telemetry reading ingested successfully",
            "reading_id": reading.reading_id
        }, status=status.HTTP_201_CREATED)

# ============================================================================
# MODULE 2 & 3: Energy Analytics & Visualization Dashboard
# ============================================================================
class DashboardSummaryAPIView(APIView):
    def get(self, request):
        total_facilities = Facility.objects.count()
        total_meters = Meter.objects.count()
        active_meters = Meter.objects.filter(status='Active').count()
        warning_meters = Meter.objects.filter(status='Warning').count()

        latest_readings = TelemetryReading.objects.order_by('-reading_timestamp')[:10]
        current_demand_kw = sum([float(r.active_power_kw) for r in latest_readings]) if latest_readings else 850.0
        avg_power_factor = (sum([float(r.power_factor) for r in latest_readings]) / len(latest_readings)) if latest_readings else 0.955

        monthly_spend = UtilityBill.objects.aggregate(total=Sum('billed_amount_inr'))['total'] or Decimal('38950000.00')
        total_solar_kw = RenewableSystem.objects.filter(system_type__icontains='Solar').aggregate(total=Sum('capacity_kw'))['total'] or Decimal('870.00')
        total_bess_kw = RenewableSystem.objects.filter(system_type__icontains='Battery').aggregate(total=Sum('capacity_kw'))['total'] or Decimal('400.00')

        open_recommendations = Recommendation.objects.filter(status__in=['Proposed', 'Approved']).count()
        total_annual_savings_potential = Recommendation.objects.filter(status__in=['Proposed', 'Approved']).aggregate(total=Sum('estimated_annual_savings_inr'))['total'] or Decimal('5890000.00')

        return Response({
            "status": "success",
            "kpis": {
                "total_facilities": total_facilities,
                "total_meters": total_meters,
                "active_meters": active_meters,
                "warning_meters": warning_meters,
                "current_grid_demand_kw": round(current_demand_kw, 1),
                "average_power_factor": round(avg_power_factor, 3),
                "total_solar_capacity_kw": float(total_solar_kw),
                "total_bess_capacity_kw": float(total_bess_kw),
                "renewable_penetration_pct": 28.5,
                "monthly_spend_inr": float(monthly_spend),
                "open_recommendations": open_recommendations,
                "annual_savings_potential_inr": float(total_annual_savings_potential),
                "carbon_intensity_kg_per_kwh": 0.62
            }
        })

class AnalyticsOverviewAPIView(APIView):
    def get(self, request):
        facility_id = request.query_params.get('facility_id', 1)
        meters = Meter.objects.filter(facility_id=facility_id)
        meter_ids = meters.values_list('meter_id', flat=True)
        readings = TelemetryReading.objects.filter(meter_id__in=meter_ids).order_by('reading_timestamp')[:24]

        hourly_series = []
        for r in readings:
            hourly_series.append({
                "timestamp": r.reading_timestamp.strftime('%H:00'),
                "active_power_kw": float(r.active_power_kw),
                "power_factor": float(r.power_factor),
                "voltage": float(r.voltage_v),
                "frequency": float(r.frequency_hz)
            })

        return Response({
            "status": "success",
            "facility_id": facility_id,
            "data_points": len(hourly_series),
            "series": hourly_series
        })

# ============================================================================
# MODULE 4: Energy Benchmarking (BEE Star Ratings)
# ============================================================================
class BenchmarkViewSet(viewsets.ModelViewSet):
    queryset = Benchmark.objects.all().order_by('benchmark_id')
    serializer_class = BenchmarkSerializer

class FacilityBenchmarkCompareAPIView(APIView):
    def get(self, request, facility_id):
        facility = Facility.objects.filter(facility_id=facility_id).first()
        if not facility:
            return Response({"error": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

        area_sqm = float(facility.total_area_sqft) * 0.092903
        bills = UtilityBill.objects.filter(facility=facility)
        if bills.exists():
            annual_kwh = sum([float(b.units_consumed_kwh) for b in bills])
        else:
            annual_kwh = float(facility.baseline_kwh_per_sqm) * area_sqm

        epi = round(annual_kwh / area_sqm, 2) if area_sqm > 0 else 0.0

        benchmark = Benchmark.objects.filter(facility_type__icontains=facility.facility_type).first()
        if not benchmark:
            benchmark = Benchmark.objects.first()

        if epi <= float(benchmark.bee_star_5_max):
            stars = 5
            rating_label = "5 Star (Exceptional Energy Efficiency)"
        elif epi <= float(benchmark.bee_star_4_max):
            stars = 4
            rating_label = "4 Star (High Efficiency)"
        elif epi <= float(benchmark.bee_star_3_max):
            stars = 3
            rating_label = "3 Star (Standard Compliant)"
        elif epi <= float(benchmark.bee_star_2_max):
            stars = 2
            rating_label = "2 Star (Moderate Efficiency - Retrofit Advised)"
        else:
            stars = 1
            rating_label = "1 Star (Poor Efficiency - Action Required)"

        return Response({
            "status": "success",
            "facility": {
                "id": facility.facility_id,
                "name": facility.name,
                "city": facility.city,
                "type": facility.facility_type,
                "area_sqft": float(facility.total_area_sqft),
                "area_sqm": round(area_sqm, 2)
            },
            "benchmarking": {
                "calculated_epi_kwh_sqm_yr": epi,
                "standard_industry_epi": float(benchmark.standard_epi_kwh_sqm_yr),
                "variance_percent": round(((epi - float(benchmark.standard_epi_kwh_sqm_yr)) / float(benchmark.standard_epi_kwh_sqm_yr)) * 100, 1),
                "bee_star_rating": stars,
                "rating_label": rating_label,
                "reference_standard": benchmark.reference_standard
            }
        })

# ============================================================================
# MODULE 5: Utility Bill Management
# ============================================================================
class UtilityProviderViewSet(viewsets.ModelViewSet):
    queryset = UtilityProvider.objects.all().order_by('provider_id')
    serializer_class = UtilityProviderSerializer

class UtilityBillViewSet(viewsets.ModelViewSet):
    queryset = UtilityBill.objects.select_related('facility', 'provider', 'verified_by').all().order_by('bill_id')
    serializer_class = UtilityBillSerializer

class BillVerifyAPIView(APIView):
    def post(self, request, bill_id):
        bill = UtilityBill.objects.filter(bill_id=bill_id).first()
        if not bill:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)

        bill.payment_status = 'Verified'
        user_id = request.data.get('user_id', 1)
        user = UserAccount.objects.filter(user_id=user_id).first()
        if user:
            bill.verified_by = user
        bill.save()

        return Response({
            "status": "success",
            "message": f"Bill {bill.bill_number} successfully verified",
            "bill_id": bill.bill_id,
            "status": bill.payment_status
        })

# ============================================================================
# MODULE 6: Energy Efficiency Recommendations
# ============================================================================
class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.select_related('facility').all().order_by('recommendation_id')
    serializer_class = RecommendationSerializer

class RecommendationStatusUpdateAPIView(APIView):
    def patch(self, request, rec_id):
        rec = Recommendation.objects.filter(recommendation_id=rec_id).first()
        if not rec:
            return Response({"error": "Recommendation not found"}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status in ['Proposed', 'Under Review', 'Approved', 'Implemented', 'Rejected']:
            rec.status = new_status
            rec.save(update_fields=['status'])
            return Response({"status": "success", "recommendation_id": rec.recommendation_id, "new_status": rec.status})
        return Response({"error": "Invalid status transition"}, status=status.HTTP_400_BAD_REQUEST)

# ============================================================================
# MODULE 7: Renewable Energy & Smart Grid
# ============================================================================
class RenewableSystemViewSet(viewsets.ModelViewSet):
    queryset = RenewableSystem.objects.select_related('facility').all().order_by('system_id')
    serializer_class = RenewableSystemSerializer

class RenewableGenerationLogViewSet(viewsets.ModelViewSet):
    queryset = RenewableGenerationLog.objects.select_related('system').order_by('-log_timestamp')
    serializer_class = RenewableGenerationLogSerializer

class DemandResponseEventViewSet(viewsets.ModelViewSet):
    queryset = DemandResponseEvent.objects.select_related('facility').all().order_by('event_id')
    serializer_class = DemandResponseEventSerializer

class TriggerDemandResponseAPIView(APIView):
    def post(self, request):
        facility_id = request.data.get('facility_id', 1)
        facility = Facility.objects.filter(facility_id=facility_id).first()
        if not facility:
            return Response({"error": "Facility not found"}, status=status.HTTP_404_NOT_FOUND)

        target_shed = Decimal(str(request.data.get('target_shed_kw', 150.0)))
        actual_shed = target_shed * Decimal('0.98')
        incentive = actual_shed * Decimal('120.00')

        now = timezone.now()
        event = DemandResponseEvent.objects.create(
            facility=facility,
            event_title=f"Smart Grid ADR - {facility.facility_code}",
            target_shed_kw=target_shed,
            actual_shed_kw=actual_shed,
            start_time=now,
            end_time=now + datetime.timedelta(hours=2),
            incentive_earned_inr=incentive,
            status='Completed'
        )

        return Response({
            "status": "success",
            "message": "Demand response event executed successfully",
            "event_id": event.event_id,
            "actual_shed_kw": float(actual_shed),
            "incentive_earned_inr": float(incentive)
        })
