# GreenGrid REST API Catalog
## Base URL: `http://127.0.0.1:8000/api/`

---

## 1. Authentication & Access Control

### `POST /api/auth/login/`
Authenticates a user and returns role permissions.
- **Request:**
  ```json
  {
    "username": "admin_greengrid",
    "password": "placeholder_password"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "status": "success",
    "message": "Authentication successful",
    "user": {
      "user_id": 1,
      "username": "admin_greengrid",
      "full_name": "Rajesh K. Sharma",
      "email": "admin@greengrid.in",
      "role": "Administrator"
    },
    "token": "greengrid_token_admin_greengrid_1"
  }
  ```

---

## 2. Facilities & Hardware Meters

### `GET /api/facilities/`
Retrieves all registered commercial and industrial facilities.

### `GET /api/meters/`
Retrieves meters. Supports filtering: `?facility_id=1` or `?status=Active`.

### `POST /api/telemetry/ingest/`
Hardware Modbus/BMS telemetry ingestion endpoint.
- **Request:**
  ```json
  {
    "meter_id": 1,
    "reading_timestamp": "2026-11-20T12:00:00Z",
    "active_power_kw": 890.4,
    "reactive_power_kvar": 210.0,
    "voltage_v": 415.2,
    "current_a": 1250.0,
    "power_factor": 0.974,
    "frequency_hz": 50.01,
    "cumulative_energy_kwh": 1290500.0
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "status": "success",
    "message": "Telemetry reading ingested successfully",
    "reading_id": 142
  }
  ```

---

## 3. Analytics & Benchmarking

### `GET /api/analytics/summary/`
High-level operational and executive KPI aggregator.

### `GET /api/benchmarks/compare/<facility_id>/`
Calculates Energy Performance Index (EPI in $kWh/m^2/year$) and evaluates BEE Star Rating.
- **Response (200 OK):**
  ```json
  {
    "status": "success",
    "facility": {
      "id": 1,
      "name": "Manyata Tech Park Tower 7",
      "area_sqm": 23225.75
    },
    "benchmarking": {
      "calculated_epi_kwh_sqm_yr": 142.5,
      "standard_industry_epi": 140.0,
      "variance_percent": 1.8,
      "bee_star_rating": 4,
      "rating_label": "4 Star (High Efficiency)",
      "reference_standard": "BEE Energy Conservation Code"
    }
  }
  ```

---

## 4. Utility Bills & Verification

### `GET /api/bills/`
Lists all monthly Discom invoices.

### `POST /api/bills/<bill_id>/verify/`
Marks a pending utility invoice as verified.
- **Request:** `{"user_id": 2}`
- **Response (200 OK):** `{"status": "success", "bill_id": 1, "status": "Verified"}`

---

## 5. Efficiency Recommendations & Smart Grid

### `PATCH /api/recommendations/<rec_id>/status/`
Updates recommendation status (`Proposed` -> `Approved` -> `Implemented`).

### `POST /api/demand-response/trigger/`
Executes an Automated Demand Response (ADR) curtailment event.
- **Request:** `{"facility_id": 1, "target_shed_kw": 180.0}`
- **Response (200 OK):**
  ```json
  {
    "status": "success",
    "event_id": 5,
    "actual_shed_kw": 176.4,
    "incentive_earned_inr": 21168.0
  }
  ```
