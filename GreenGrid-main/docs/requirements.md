# GreenGrid: Software Requirements Specification (SRS)
## Project Code: P02 | Domain: Energy
**Track:** Python Full Stack Development (Django + React + MySQL)  
**Total Duration:** 90 Hours (Sprint 0: 6h, Sprints 1-3: 28h each)

---

## 1. Project Overview & Scope
**GreenGrid** is a centralized web-based Energy Management Information System (EMIS) designed to monitor, analyze, and optimize energy consumption across multi-facility commercial and industrial estates. It connects smart hardware meters and Building Management Systems (BMS), benchmarks energy performance against national standards (Bureau of Energy Efficiency - BEE), manages Discom utility bills, provides algorithmic energy efficiency retrofits, and interfaces with on-site renewable energy systems (Solar PV, BESS) and smart grids.

---

## 2. Module Breakdown & User Stories

### Module 1: Data Acquisition & Integration
- **P02-US01**: *As a Field Engineer*, I want to register and commission hardware smart energy meters (Modbus TCP/IP) associated with specific facilities so that telemetry data can be ingested.
- **P02-US02**: *As a System Gateway*, I want to POST batch telemetry packets (Active Power kW, Reactive Power kVAR, Voltage, Current, Frequency, PF) to `/api/telemetry/ingest/` with millisecond timestamps.

### Module 2: Energy Analytics
- **P02-US03**: *As a Facility Manager*, I want to analyze diurnal load demand curves to identify peak hours and seasonal variance.
- **P02-US04**: *As an Energy Auditor*, I want to detect low displacement power factor (< 0.92) across inductive machinery feeders to eliminate Discom reactive surcharge penalties.

### Module 3: Visualization & Centralized Dashboard
- **P02-US05**: *As an Executive*, I want a high-level KPI dashboard displaying active grid demand, renewable penetration %, total facilities, and monthly electricity expenditure in INR (₹).

### Module 4: Energy Benchmarking (BEE Standards)
- **P02-US06**: *As an Auditor*, I want to compute the Energy Performance Index (EPI in $kWh/m^2/year$) by comparing annual energy draw against total built-up floor area.
- **P02-US07**: *As a Manager*, I want to benchmark our facility against national BEE Star Rating standards (1 to 5 Stars) to satisfy statutory compliance.

### Module 5: Utility Bill Management
- **P02-US08**: *As an Accountant*, I want to log and track monthly Discom utility invoices (BESCOM, MSEDCL, TSSPDCL) with peak/off-peak tariff breakdowns.
- **P02-US09**: *As a Facility Manager*, I want to verify billed amounts against metered telemetry before approving payments.

### Module 6: Energy Efficiency Recommendations
- **P02-US10**: *As a Facility Manager*, I want automated recommendations detailing specific energy-saving retrofits (VFDs, APFC capacitor banks, LED motion sensors), implementation costs, and payback periods in months.
- **P02-US11**: *As an Admin*, I want to transition recommendation statuses from `Proposed` to `Approved` and `Implemented`.

### Module 7: Renewable Energy & Smart Grid Integration
- **P02-US12**: *As an Operator*, I want real-time visibility into rooftop Solar PV generation, net-metering grid exports, and Battery Energy Storage System (BESS) State of Charge (SOC %).
- **P02-US13**: *As a Grid Operator*, I want to participate in Automated Demand Response (ADR) events to shed non-critical load during grid emergencies and earn financial incentives.

### Module 8: User Management & Access Control (RBAC)
- **P02-US14**: *As an Administrator*, I want role-based access control governing permissions across Administrator, Facility Manager, Field Engineer, and Auditor accounts.

---

## 3. Agile Sprint Mapping (90-Hour Schedule)

| Sprint | Duration | Deliverables & Focus | Git Tag |
| :--- | :--- | :--- | :--- |
| **Sprint 0** | 6 Hours | Git repository setup, 3NF MySQL schema design, wireframes, project skeleton, JWT authentication | `v0.1.0` |
| **Sprint 1** | 28 Hours | Data Acquisition APIs, Meter registry, Central Dashboard UI, Initial Telemetry Ingestion tests | `v0.2.0` |
| **Sprint 2** | 28 Hours | Energy Analytics, Power Factor compensation, BEE Benchmarking, Utility Bill management | `v0.3.0` |
| **Sprint 3** | 28 Hours | Recommendations engine, Renewable integration, Smart Grid ADR, full test suite & documentation | `v1.0.0` |
