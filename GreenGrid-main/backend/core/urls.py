"""
URL routing for GreenGrid Core Application
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, UserAccountViewSet, LoginAPIView,
    FacilityViewSet, MeterViewSet, TelemetryReadingViewSet, DataIngestAPIView,
    DashboardSummaryAPIView, AnalyticsOverviewAPIView,
    BenchmarkViewSet, FacilityBenchmarkCompareAPIView,
    UtilityProviderViewSet, UtilityBillViewSet, BillVerifyAPIView,
    RecommendationViewSet, RecommendationStatusUpdateAPIView,
    RenewableSystemViewSet, RenewableGenerationLogViewSet,
    DemandResponseEventViewSet, TriggerDemandResponseAPIView
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'users', UserAccountViewSet)
router.register(r'facilities', FacilityViewSet)
router.register(r'meters', MeterViewSet)
router.register(r'telemetry', TelemetryReadingViewSet)
router.register(r'benchmarks', BenchmarkViewSet)
router.register(r'providers', UtilityProviderViewSet)
router.register(r'bills', UtilityBillViewSet)
router.register(r'recommendations', RecommendationViewSet)
router.register(r'renewables', RenewableSystemViewSet)
router.register(r'renewable-logs', RenewableGenerationLogViewSet)
router.register(r'demand-response', DemandResponseEventViewSet)

urlpatterns = [
    # Custom Endpoints
    path('auth/login/', LoginAPIView.as_view(), name='api-login'),
    path('telemetry/ingest/', DataIngestAPIView.as_view(), name='api-telemetry-ingest'),
    path('analytics/summary/', DashboardSummaryAPIView.as_view(), name='api-analytics-summary'),
    path('analytics/overview/', AnalyticsOverviewAPIView.as_view(), name='api-analytics-overview'),
    path('benchmarks/compare/<int:facility_id>/', FacilityBenchmarkCompareAPIView.as_view(), name='api-benchmark-compare'),
    path('bills/<int:bill_id>/verify/', BillVerifyAPIView.as_view(), name='api-bill-verify'),
    path('recommendations/<int:rec_id>/status/', RecommendationStatusUpdateAPIView.as_view(), name='api-rec-status'),
    path('demand-response/trigger/', TriggerDemandResponseAPIView.as_view(), name='api-dr-trigger'),

    # Default router endpoints
    path('', include(router.urls)),
]
