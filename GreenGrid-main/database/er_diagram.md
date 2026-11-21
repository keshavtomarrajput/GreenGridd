# GreenGrid: Entity Relationship (ER) Summary
## Relational Database Schema (3NF) - MySQL 8.0

---

## 1. ER Diagram (Mermaid)

```mermaid
erDiagram
    ROLES ||--o{ USERS : "has assigned (1:N)"
    USERS ||--o{ FACILITIES : "manages (1:N)"
    USERS ||--o{ UTILITY_BILLS : "verifies (1:N)"
    FACILITIES ||--o{ METERS : "contains (1:N)"
    FACILITIES ||--o{ UTILITY_BILLS : "incurs (1:N)"
    FACILITIES ||--o{ RECOMMENDATIONS : "generates (1:N)"
    FACILITIES ||--o{ RENEWABLE_SYSTEMS : "hosts (1:N)"
    FACILITIES ||--o{ DEMAND_RESPONSE_EVENTS : "participates (1:N)"
    METERS ||--o{ TELEMETRY_READINGS : "records (1:N)"
    UTILITY_PROVIDERS ||--o{ UTILITY_BILLS : "issues (1:N)"
    RENEWABLE_SYSTEMS ||--o{ RENEWABLE_GENERATION_LOGS : "produces (1:N)"
    BENCHMARKS ||--o{ FACILITIES : "classifies by type & climate (1:N)"

    ROLES {
        int role_id PK
        string role_name UK
        string role_description
    }

    USERS {
        int user_id PK
        string username UK
        string email UK
        string password_hash
        string full_name
        string phone_number
        int role_id FK
        boolean is_active
    }

    FACILITIES {
        int facility_id PK
        string facility_code UK
        string name
        string facility_type
        string city
        string state
        decimal total_area_sqft
        int manager_id FK
    }

    METERS {
        int meter_id PK
        string meter_serial_no UK
        int facility_id FK
        string meter_name
        string meter_type
        string status
        string ip_address
    }

    TELEMETRY_READINGS {
        bigint reading_id PK
        int meter_id FK
        datetime reading_timestamp
        decimal active_power_kw
        decimal reactive_power_kvar
        decimal power_factor
        decimal cumulative_energy_kwh
    }

    BENCHMARKS {
        int benchmark_id PK
        string facility_type
        string climate_zone
        decimal standard_epi_kwh_sqm_yr
        decimal bee_star_5_max
    }

    UTILITY_PROVIDERS {
        int provider_id PK
        string provider_name UK
        string state
        string tariff_code
    }

    UTILITY_BILLS {
        int bill_id PK
        int facility_id FK
        int provider_id FK
        string bill_number UK
        int billing_month
        int billing_year
        decimal units_consumed_kwh
        decimal billed_amount_inr
        int verified_by FK
    }

    RECOMMENDATIONS {
        int recommendation_id PK
        int facility_id FK
        string title
        string category
        decimal estimated_annual_savings_inr
        decimal implementation_cost_inr
        decimal payback_period_months
        string status
    }

    RENEWABLE_SYSTEMS {
        int system_id PK
        int facility_id FK
        string system_type
        decimal capacity_kw
        string status
    }

    RENEWABLE_GENERATION_LOGS {
        bigint log_id PK
        int system_id FK
        datetime log_timestamp
        decimal generation_kwh
        decimal battery_charge_kwh
        decimal grid_export_kwh
    }

    DEMAND_RESPONSE_EVENTS {
        int event_id PK
        int facility_id FK
        string event_title
        decimal target_shed_kw
        decimal actual_shed_kw
        decimal incentive_earned_inr
        string status
    }
```

---

## 2. Table Relationships (Cardinality Breakdown)

| Parent Table | Child Table | Relationship | Description | Foreign Key Constraint |
| :--- | :--- | :--- | :--- | :--- |
| `roles` | `users` | **1 : N (One-to-Many)** | One role (Admin, Manager, Engineer) can be assigned to multiple users. | `fk_users_role` (`ON DELETE RESTRICT`) |
| `users` | `facilities` | **1 : N (One-to-Many)** | A facility manager can oversee multiple facilities. | `fk_facilities_manager` (`ON DELETE SET NULL`) |
| `facilities` | `meters` | **1 : N (One-to-Many)** | A facility houses multiple sub-meters (Chillers, Incomers, UPS, Solar). | `fk_meters_facility` (`ON DELETE CASCADE`) |
| `meters` | `telemetry_readings` | **1 : N (One-to-Many)** | One meter streams thousands of time-series readings. | `fk_telemetry_meter` (`ON DELETE CASCADE`) |
| `utility_providers` | `utility_bills` | **1 : N (One-to-Many)** | A utility Discom (e.g. BESCOM) issues bills to multiple facilities. | `fk_bills_provider` (`ON DELETE RESTRICT`) |
| `facilities` | `utility_bills` | **1 : N (One-to-Many)** | Each facility receives monthly bills over multiple fiscal years. | `fk_bills_facility` (`ON DELETE RESTRICT`) |
| `users` | `utility_bills` | **1 : N (One-to-Many)** | A manager verifies/approves multiple utility invoices. | `fk_bills_verifier` (`ON DELETE SET NULL`) |
| `facilities` | `recommendations` | **1 : N (One-to-Many)** | An energy audit produces multiple efficiency retrofit recommendations. | `fk_recs_facility` (`ON DELETE CASCADE`) |
| `facilities` | `renewable_systems` | **1 : N (One-to-Many)** | A facility can operate rooftop solar, BESS batteries, and wind systems. | `fk_renewables_facility` (`ON DELETE CASCADE`) |
| `renewable_systems` | `renewable_generation_logs` | **1 : N (One-to-Many)** | Each renewable asset logs generation and net-metering telemetry. | `fk_renlogs_system` (`ON DELETE CASCADE`) |
| `facilities` | `demand_response_events` | **1 : N (One-to-Many)** | A facility participates in scheduled grid demand-response events. | `fk_drevents_facility` (`ON DELETE CASCADE`) |
| `benchmarks` | `facilities` | **Conceptual 1 : N** | Standard BEE performance standards classify facilities by type and climate. | Lookup via `facility_type` |

---

## 3. Normal Form Compliance (3NF Analysis)
1. **1NF (First Normal Form)**:
   - All columns contain atomic, indivisible values.
   - Every table possesses an explicit primary key (`role_id`, `user_id`, `facility_id`, etc.).
   - No repeating groups or comma-delimited arrays exist.

2. **2NF (Second Normal Form)**:
   - Full functional dependency: All non-key attributes depend completely on the primary key, with no partial dependencies on compound keys.

3. **3NF (Third Normal Form)**:
   - No transitive dependencies: Non-key attributes depend only on the primary key and not on other non-key attributes. For example, utility provider details (`tariff_code`, `customer_care_no`) reside in `utility_providers`, not repeated redundantly in `utility_bills`.
