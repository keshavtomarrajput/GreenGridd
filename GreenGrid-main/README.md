# 🌱 GreenGrid: Smart Energy Management for Tomorrow's Needs
## Project Code: P02 | Domain: Energy
**Technology Stack:** Python, Django 4.2 LTS / 5.2, Django REST Framework, React 18, MySQL 8.0 Database  
**Git Repository:** `mca2-fsdpython-greengrid`  
**Primary Users:** Customer (Facility Manager) and Field Engineer  
**Live URL:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## ⚡ Live Status
The server is currently **LIVE and RUNNING** on your system:
- 👉 **Web Application & EMIS Dashboard:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- 👉 **API Documentation Directory:** [http://127.0.0.1:8000/api-info/](http://127.0.0.1:8000/api-info/)
- 👉 **Django Administration:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 🚀 How to Relaunch in Future

Simply double-click:
👉 **`run_greengrid.bat`** inside `C:\Users\one\Desktop\Project1\GreenGrid\`

Or via terminal:
```bash
cd C:\Users\one\Desktop\Project1\GreenGrid\backend
..\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

---

## 📂 Project Structure & Artifacts

- **`backend/`**: Django REST Framework backend with all 8 energy management modules.
  - `config/settings.py`: Configured with MySQL 8.0 (`greengrid_db`, user: `root`).
  - `core/models.py`: 3NF Normalized schema with 12 entities (Facilities, Meters, Telemetry, Benchmarks, Bills, Recommendations, Renewables, Roles, Users).
  - `core/views.py`: REST APIs + interactive dashboard controller.
  - `templates/index.html`: Complete responsive web interface.
- **`database/`**:
  - `schema.sql`: Complete MySQL 8.0 3NF DDL script.
  - `seed_data.sql`: Realistic Indian-context dataset (Bengaluru, Pune, Hyderabad, BESCOM, MSEDCL, INR).
  - `er_diagram.md`: Full Mermaid ER diagram and table relationships.
- **`docs/`**:
  - `requirements.md`: SRS, User stories, and 90-hour Agile sprint mapping (`v0.1.0` to `v1.0.0`).
  - `api_docs.md`: Complete REST API catalog with request/response samples.
  - `test_report.md`: Automated test execution report.
- **`frontend/`**: React 18 application with Vite.

---

## 📦 8 Project Modules Covered

1. **Data Acquisition & Integration**: Modbus TCP/IP gateway ingestion (`POST /api/telemetry/ingest/`), smart meters registry.
2. **Energy Analytics**: Load demand curves, active vs reactive power, power factor tracking.
3. **Visualization & Dashboard**: Centralized multi-facility oversight, real-time demand, monthly spend.
4. **Energy Benchmarking**: Bureau of Energy Efficiency (BEE) Indian Star Rating standard (1 to 5 Stars) and EPI ($kWh/m^2/year$).
5. **Utility Bill Management**: Monthly Discom billing audits (BESCOM, MSEDCL, TSSPDCL), INR ₹ spend verification.
6. **Energy Efficiency Recommendations**: Algorithmic retrofits, Capex, annual savings in INR, payback period in months.
7. **Renewables & Smart Grid**: Rooftop Solar PV, Battery Storage (BESS SOC %), Automated Demand Response (ADR) load-shedding trigger.
8. **User Management & Access Control**: Role-Based Access Control (Administrator, Facility Manager, Field Engineer).
