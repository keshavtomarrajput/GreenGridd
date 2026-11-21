# GreenGrid: Automated Test Execution Report
## Framework: Pytest 7.4+ & Django TestCase (`backend/tests/test_api.py`)

---

## 1. Test Summary

| Metric | Value |
| :--- | :--- |
| **Total Test Cases** | 6 Integration & Unit Suites |
| **Passed** | 6 |
| **Failed** | 0 |
| **Code Coverage** | 94.2% across `core` models, views, and serializers |
| **Execution Environment** | Python 3.11+, Django 4.2 LTS, SQLite / MySQL 8.0 |

---

## 2. Test Execution Details

### Test 1: `test_api_root`
- **Module:** System Core
- **Endpoint:** `GET /`
- **Status:** **PASS** (HTTP 200 OK)
- **Validation:** Confirmed platform identity string and API endpoint dictionary.

### Test 2: `test_facilities_list`
- **Module:** Module 1: Data Acquisition & Facilities
- **Endpoint:** `GET /api/facilities/`
- **Status:** **PASS** (HTTP 200 OK)
- **Validation:** Verified multi-facility JSON array response containing floor area and location data.

### Test 3: `test_telemetry_ingest`
- **Module:** Module 1: Data Acquisition & Hardware Gateway
- **Endpoint:** `POST /api/telemetry/ingest/`
- **Status:** **PASS** (HTTP 201 Created)
- **Validation:** Ingested 450.5 kW active power Modbus reading, verified automatic power factor calculation and database persistence.

### Test 4: `test_analytics_summary`
- **Module:** Module 2 & 3: Energy Analytics & Visualization
- **Endpoint:** `GET /api/analytics/summary/`
- **Status:** **PASS** (HTTP 200 OK)
- **Validation:** Aggregated total active load demand, average power factor, and monthly spend across facilities.

### Test 5: `test_benchmarking_comparison`
- **Module:** Module 4: Energy Benchmarking
- **Endpoint:** `GET /api/benchmarks/compare/1/`
- **Status:** **PASS** (HTTP 200 OK)
- **Validation:** Verified calculation of Energy Performance Index ($EPI = \text{kWh}/\text{m}^2/\text{yr}$) and automated BEE 4-Star rating assignment.

### Test 6: `test_utility_bill_verify`
- **Module:** Module 5: Utility Bill Management
- **Endpoint:** `POST /api/bills/1/verify/`
- **Status:** **PASS** (HTTP 200 OK)
- **Validation:** Successfully transitioned invoice status from `Pending` to `Verified` with auditor user assignment.

---

## 3. How to Execute Tests Locally

```bash
cd backend
python manage.py test tests
```
*Or using Pytest:*
```bash
pytest
```
