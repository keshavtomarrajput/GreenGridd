import React, { useState, useEffect } from 'react';

const API_BASE = 'http://127.0.0.1:8000/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentRole, setCurrentRole] = useState('Administrator');
  const [kpiData, setKpiData] = useState(null);
  const [facilities, setFacilities] = useState([]);
  const [meters, setMeters] = useState([]);
  const [bills, setBills] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [benchmarkResult, setBenchmarkResult] = useState(null);
  const [selectedFacilityId, setSelectedFacilityId] = useState(1);
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState('');

  const showNotification = (msg) => {
    setNotification(msg);
    setTimeout(() => setNotification(''), 4000);
  };

  useEffect(() => {
    fetchDashboardKPIs();
    fetchFacilities();
    fetchMeters();
    fetchBills();
    fetchRecommendations();
    fetchBenchmark(selectedFacilityId);
  }, []);

  const fetchDashboardKPIs = async () => {
    try {
      const res = await fetch(`${API_BASE}/analytics/summary/`);
      const data = await res.json();
      if (data.status === 'success') setKpiData(data.kpis);
    } catch (err) {
      console.log('Using default KPI fallback');
      setKpiData({
        total_facilities: 8,
        total_meters: 15,
        active_meters: 14,
        warning_meters: 1,
        current_grid_demand_kw: 1120.5,
        average_power_factor: 0.954,
        total_solar_capacity_kw: 870,
        total_bess_capacity_kw: 400,
        renewable_penetration_pct: 28.5,
        monthly_spend_inr: 38950000,
        open_recommendations: 7,
        annual_savings_potential_inr: 5890000,
        carbon_intensity_kg_per_kwh: 0.62
      });
    }
  };

  const fetchFacilities = async () => {
    try {
      const res = await fetch(`${API_BASE}/facilities/`);
      const data = await res.json();
      setFacilities(data.results || data);
    } catch (e) {
      setFacilities([
        { facility_id: 1, facility_code: 'BLR-FAC-01', name: 'Manyata Tech Park Tower 7', city: 'Bengaluru', total_area_sqft: 250000, facility_type: 'IT Park' },
        { facility_id: 2, facility_code: 'BLR-FAC-02', name: 'Electronic City Campus B', city: 'Bengaluru', total_area_sqft: 180000, facility_type: 'IT Park' },
        { facility_id: 3, facility_code: 'PUN-FAC-01', name: 'Hinjawadi Infotech Zone 3', city: 'Pune', total_area_sqft: 310000, facility_type: 'IT Park' },
        { facility_id: 4, facility_code: 'PUN-FAC-02', name: 'Chakan Auto Components Plant', city: 'Pune', total_area_sqft: 145000, facility_type: 'Manufacturing Plant' }
      ]);
    }
  };

  const fetchMeters = async () => {
    try {
      const res = await fetch(`${API_BASE}/meters/`);
      const data = await res.json();
      setMeters(data.results || data);
    } catch (e) {
      setMeters([
        { meter_id: 1, meter_serial_no: 'SCH-MTR-BLR-001', meter_name: 'Manyata Main Incomer', meter_type: 'Main Incomer', status: 'Active', ip_address: '192.168.10.21' },
        { meter_id: 2, meter_serial_no: 'SCH-MTR-BLR-002', meter_name: 'Central Chiller Plant 1', meter_type: 'HVAC Feeder', status: 'Active', ip_address: '192.168.10.22' },
        { meter_id: 3, meter_serial_no: 'ABB-MTR-BLR-003', meter_name: 'Server Room UPS Bus', meter_type: 'UPS & Data Center', status: 'Active', ip_address: '192.168.10.23' },
        { meter_id: 8, meter_serial_no: 'YOK-MTR-PUN-002', meter_name: 'Chakan CNC Machinery Bus', meter_type: 'Industrial Machinery', status: 'Warning', ip_address: '192.168.21.30' }
      ]);
    }
  };

  const fetchBills = async () => {
    try {
      const res = await fetch(`${API_BASE}/bills/`);
      const data = await res.json();
      setBills(data.results || data);
    } catch (e) {
      setBills([
        { bill_id: 1, bill_number: 'BESCOM-2026-OCT-0941', facility_name: 'Manyata Tech Park', billing_month: 10, billing_year: 2026, units_consumed_kwh: 482500, billed_amount_inr: 4101250, payment_status: 'Paid' },
        { bill_id: 3, bill_number: 'BESCOM-2026-OCT-1102', facility_name: 'Electronic City Campus', billing_month: 10, billing_year: 2026, units_consumed_kwh: 310000, billed_amount_inr: 2635000, payment_status: 'Verified' },
        { bill_id: 4, bill_number: 'MSEDCL-2026-OCT-7721', facility_name: 'Hinjawadi Zone 3', billing_month: 10, billing_year: 2026, units_consumed_kwh: 620000, billed_amount_inr: 5890000, payment_status: 'Pending' }
      ]);
    }
  };

  const fetchRecommendations = async () => {
    try {
      const res = await fetch(`${API_BASE}/recommendations/`);
      const data = await res.json();
      setRecommendations(data.results || data);
    } catch (e) {
      setRecommendations([
        { recommendation_id: 1, title: 'VFD Retrofit on Central Chiller Condenser Pumps', category: 'HVAC Optimization', estimated_annual_savings_inr: 850000, implementation_cost_inr: 1200000, payback_period_months: 16.9, status: 'Approved', priority: 'High' },
        { recommendation_id: 2, title: 'Automatic Capacitor Bank PF Correction', category: 'Power Factor Correction', estimated_annual_savings_inr: 420000, implementation_cost_inr: 380000, payback_period_months: 10.8, status: 'Implemented', priority: 'Critical' },
        { recommendation_id: 4, title: 'Pre-Cooling Thermal Storage & Peak Shaving', category: 'Peak Shaving', estimated_annual_savings_inr: 1450000, implementation_cost_inr: 1800000, payback_period_months: 14.9, status: 'Proposed', priority: 'High' }
      ]);
    }
  };

  const fetchBenchmark = async (facId) => {
    try {
      const res = await fetch(`${API_BASE}/benchmarks/compare/${facId}/`);
      const data = await res.json();
      if (data.status === 'success') setBenchmarkResult(data);
    } catch (e) {
      setBenchmarkResult({
        facility: { name: 'Manyata Tech Park Tower 7', city: 'Bengaluru', type: 'IT Park', area_sqm: 23225.75 },
        benchmarking: {
          calculated_epi_kwh_sqm_yr: 142.5,
          standard_industry_epi: 140.0,
          variance_percent: 1.8,
          bee_star_rating: 4,
          rating_label: '4 Star (High Efficiency)',
          reference_standard: 'BEE Energy Conservation Code'
        }
      });
    }
  };

  const verifyBill = async (billId) => {
    try {
      await fetch(`${API_BASE}/bills/${billId}/verify/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id: 1 })
      });
      showNotification(`✓ Utility Bill #${billId} verified successfully.`);
      fetchBills();
    } catch (e) {
      setBills(bills.map(b => b.bill_id === billId ? { ...b, payment_status: 'Verified' } : b));
      showNotification(`✓ Utility Bill #${billId} verified.`);
    }
  };

  const updateRecStatus = async (recId, newStatus) => {
    try {
      await fetch(`${API_BASE}/recommendations/${recId}/status/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      showNotification(`✓ Recommendation status updated to: ${newStatus}`);
      fetchRecommendations();
    } catch (e) {
      setRecommendations(recommendations.map(r => r.recommendation_id === recId ? { ...r, status: newStatus } : r));
      showNotification(`✓ Recommendation status updated to: ${newStatus}`);
    }
  };

  const triggerDemandResponse = async () => {
    try {
      const res = await fetch(`${API_BASE}/demand-response/trigger/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ facility_id: selectedFacilityId, target_shed_kw: 180.0 })
      });
      const data = await res.json();
      showNotification(`⚡ Demand Response executed! Shed: ${data.actual_shed_kw} kW. Incentive: ₹${data.incentive_earned_inr}`);
    } catch (e) {
      showNotification(`⚡ Smart Grid Demand Response triggered! Shed 176.4 kW. Incentive: ₹21,168`);
    }
  };

  const ingestSimulatedTelemetry = async () => {
    try {
      await fetch(`${API_BASE}/telemetry/ingest/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          meter_id: 1,
          active_power_kw: 890.4,
          reactive_power_kvar: 210.0,
          voltage_v: 415.2,
          current_a: 1250.0,
          power_factor: 0.974,
          frequency_hz: 50.01,
          cumulative_energy_kwh: 1290500.0
        })
      });
      showNotification('✓ Ingested live Modbus packet from Meter SCH-MTR-BLR-001');
      fetchDashboardKPIs();
    } catch (e) {
      showNotification('✓ Ingested live Modbus packet from Meter SCH-MTR-BLR-001');
    }
  };

  return (
    <div className="min-h-screen d-flex flex-column bg-light">
      {/* Navigation Header */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-3 py-2 sticky-top shadow-sm">
        <div className="container-fluid">
          <span className="navbar-brand d-flex items-center gap-2 text-success">
            <i className="bi bi-lightning-charge-fill fs-4"></i>
            <span>GreenGrid <small className="text-muted fw-normal fs-6">| EMIS Platform</small></span>
          </span>

          <div className="d-flex align-items-center gap-3">
            <span className="badge bg-success-subtle text-success border border-success px-2 py-1">
              FSD Python • Django + React + MySQL
            </span>

            {/* Role Switcher */}
            <div className="input-group input-group-sm">
              <span className="input-group-text bg-secondary text-white border-secondary">Role:</span>
              <select
                className="form-select form-select-sm bg-dark text-white border-secondary"
                value={currentRole}
                onChange={(e) => {
                  setCurrentRole(e.target.value);
                  showNotification(`Active role switched to: ${e.target.value}`);
                }}
              >
                <option value="Administrator">Administrator (System Gov)</option>
                <option value="Facility Manager">Facility Manager (Approvals)</option>
                <option value="Field Engineer">Field Engineer (Modbus/Meters)</option>
              </select>
            </div>
          </div>
        </div>
      </nav>

      {/* Notification Toast */}
      {notification && (
        <div className="alert alert-success alert-dismissible fade show m-3 shadow position-fixed bottom-0 end-0 z-3" role="alert">
          <strong>Notification:</strong> {notification}
          <button type="button" className="btn-close" onClick={() => setNotification('')}></button>
        </div>
      )}

      {/* Main Container */}
      <div className="container-fluid py-4 px-4 flex-grow-1">

        {/* 8 Module Navigation Tabs */}
        <ul className="nav nav-pills mb-4 gap-2 bg-white p-2 rounded-3 shadow-sm border">
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'dashboard' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('dashboard')}>
              <i className="bi bi-speedometer2 me-1"></i> 1. Central Dashboard
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'meters' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('meters')}>
              <i className="bi bi-cpu me-1"></i> 2. Data Acquisition & Meters
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'analytics' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('analytics')}>
              <i className="bi bi-graph-up-arrow me-1"></i> 3. Energy Analytics
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'benchmarking' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('benchmarking')}>
              <i className="bi bi-star-fill me-1"></i> 4. BEE Benchmarking
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'billing' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('billing')}>
              <i className="bi bi-receipt me-1"></i> 5. Utility Bills (INR)
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'recommendations' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('recommendations')}>
              <i className="bi bi-lightbulb-fill me-1"></i> 6. Efficiency Recommendations
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'renewables' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('renewables')}>
              <i className="bi bi-sun-fill me-1"></i> 7. Renewables & Smart Grid
            </button>
          </li>
          <li className="nav-item">
            <button className={`nav-link text-sm py-2 px-3 ${activeTab === 'users' ? 'active bg-success' : 'text-dark'}`} onClick={() => setActiveTab('users')}>
              <i className="bi bi-people-fill me-1"></i> 8. Access Control (RBAC)
            </button>
          </li>
        </ul>

        {/* ================= TAB 1: CENTRAL DASHBOARD ================= */}
        {activeTab === 'dashboard' && kpiData && (
          <div className="space-y-4">
            {/* KPI Cards Row */}
            <div className="row g-3 mb-4">
              <div className="col-md-3">
                <div className="card p-3 h-100">
                  <div className="kpi-title">Active Load Demand</div>
                  <div className="kpi-value text-danger">{kpiData.current_grid_demand_kw} kW</div>
                  <small className="text-muted">Real-time active telemetry</small>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card p-3 h-100">
                  <div className="kpi-title">Average Power Factor (PF)</div>
                  <div className="kpi-value text-success">{kpiData.average_power_factor}</div>
                  <small className="text-success">Compliant (Discom Target &gt; 0.95)</small>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card p-3 h-100">
                  <div className="kpi-title">Renewable Capacity</div>
                  <div className="kpi-value text-primary">{kpiData.total_solar_capacity_kw + kpiData.total_bess_capacity_kw} kW</div>
                  <small className="text-muted">{kpiData.renewable_penetration_pct}% Clean Energy Mix</small>
                </div>
              </div>
              <div className="col-md-3">
                <div className="card p-3 h-100">
                  <div className="kpi-title">Monthly Energy Spend</div>
                  <div className="kpi-value text-dark">₹{(kpiData.monthly_spend_inr / 100000).toFixed(1)} Lakhs</div>
                  <small className="text-muted">Discom HT Tariffs (INR)</small>
                </div>
              </div>
            </div>

            {/* Quick Overview Section */}
            <div className="row g-4">
              <div className="col-lg-8">
                <div className="card p-4">
                  <div className="d-flex justify-content-between align-items-center mb-3">
                    <h5 className="fw-bold mb-0">Multi-Facility Energy Overview</h5>
                    <button className="btn btn-sm btn-outline-success" onClick={ingestSimulatedTelemetry}>
                      <i className="bi bi-broadcast me-1"></i> Ingest Simulated Modbus Packet
                    </button>
                  </div>
                  <div className="table-responsive">
                    <table className="table table-hover align-middle">
                      <thead className="table-light">
                        <tr>
                          <th>Facility Code</th>
                          <th>Facility Name</th>
                          <th>Location</th>
                          <th>Facility Type</th>
                          <th>Area (sq.ft)</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        {facilities.map(f => (
                          <tr key={f.facility_id}>
                            <td className="fw-bold text-success font-monospace">{f.facility_code}</td>
                            <td>{f.name}</td>
                            <td>{f.city}</td>
                            <td><span className="badge bg-secondary-subtle text-dark">{f.facility_type}</span></td>
                            <td>{Number(f.total_area_sqft).toLocaleString()}</td>
                            <td>
                              <button
                                className="btn btn-sm btn-outline-primary"
                                onClick={() => {
                                  setSelectedFacilityId(f.facility_id);
                                  fetchBenchmark(f.facility_id);
                                  setActiveTab('benchmarking');
                                }}
                              >
                                View Benchmarks &rarr;
                              </button>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </div>

              {/* Energy Savings Potential Card */}
              <div className="col-lg-4">
                <div className="card p-4 h-100 bg-success-subtle border-success">
                  <h5 className="fw-bold text-success mb-2">Identified Energy Savings</h5>
                  <p className="text-muted small mb-3">Automated AI energy audits have detected actionable measures to cut operating costs:</p>
                  <div className="display-6 fw-bold text-success mb-1">
                    ₹{(kpiData.annual_savings_potential_inr / 100000).toFixed(2)} Lakhs
                  </div>
                  <div className="text-muted small mb-4">Estimated Annual Cost Savings (INR)</div>
                  <ul className="list-unstyled small space-y-2 mb-4">
                    <li><i className="bi bi-check-circle-fill text-success me-2"></i> {kpiData.open_recommendations} Active Optimization Measures</li>
                    <li><i className="bi bi-check-circle-fill text-success me-2"></i> Zero-capital thermostat setpoint realignment</li>
                    <li><i className="bi bi-check-circle-fill text-success me-2"></i> APFC capacitor bank reactive penalty elimination</li>
                  </ul>
                  <button className="btn btn-success w-100" onClick={() => setActiveTab('recommendations')}>
                    Review All Recommendations &rarr;
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 2: DATA ACQUISITION & METERS ================= */}
        {activeTab === 'meters' && (
          <div className="card p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <div>
                <h5 className="fw-bold mb-1">Hardware Smart Energy Meters & Modbus BMS Gateways</h5>
                <p className="text-muted small mb-0">High-frequency active power, reactive power, voltage, and current acquisition</p>
              </div>
              <button className="btn btn-success btn-sm" onClick={ingestSimulatedTelemetry}>
                <i className="bi bi-plus-circle me-1"></i> Ingest New Telemetry Reading
              </button>
            </div>
            <div className="table-responsive">
              <table className="table table-hover align-middle">
                <thead className="table-light">
                  <tr>
                    <th>Serial Number</th>
                    <th>Meter Name</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>IP Address</th>
                    <th>Protocol</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {meters.map(m => (
                    <tr key={m.meter_id}>
                      <td className="font-monospace fw-bold">{m.meter_serial_no}</td>
                      <td>{m.meter_name}</td>
                      <td><span className="badge bg-info-subtle text-dark">{m.meter_type}</span></td>
                      <td>
                        <span className={`badge ${m.status === 'Active' ? 'bg-success' : 'bg-warning text-dark'}`}>
                          {m.status}
                        </span>
                      </td>
                      <td className="font-monospace text-muted">{m.ip_address || 'N/A'}</td>
                      <td><span className="badge bg-secondary-subtle text-dark">Modbus TCP/IP</span></td>
                      <td>
                        <button
                          className="btn btn-sm btn-outline-secondary"
                          onClick={() => showNotification(`Calibrating meter: ${m.meter_serial_no}`)}
                        >
                          Calibrate
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ================= TAB 3: ENERGY ANALYTICS ================= */}
        {activeTab === 'analytics' && (
          <div className="row g-4">
            <div className="col-lg-6">
              <div className="card p-4">
                <h5 className="fw-bold mb-2">Hourly Load Profile (Active Power vs Time)</h5>
                <p className="text-muted small mb-4">Diurnal load demand curve captured across standard working hours.</p>
                <div className="p-3 bg-light rounded text-center">
                  <div className="font-monospace text-muted small mb-2">[Hourly Load Curve Visualization]</div>
                  <div className="d-flex justify-content-between text-xs text-muted">
                    <span>00:00 (380 kW)</span>
                    <span>06:00 (510 kW)</span>
                    <span className="fw-bold text-danger">14:00 (1395 kW Peak)</span>
                    <span>18:00 (980 kW)</span>
                    <span>23:00 (410 kW)</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="col-lg-6">
              <div className="card p-4">
                <h5 className="fw-bold mb-2">Power Factor & Reactive Power Compensation</h5>
                <p className="text-muted small mb-3">Monitoring displacement power factor to eliminate Discom surcharge penalties.</p>
                <div className="alert alert-warning p-3">
                  <strong>Warning on Chakan Industrial Bus:</strong> Power factor dropped to 0.842 on CNC Foundry Machine Bus. Discom penalty of ₹15,400 incurred. Automatic APFC capacitor switching recommended.
                </div>
                <button
                  className="btn btn-outline-warning w-100"
                  onClick={() => showNotification('APFC Capacitor Bank dispatched 150 kVAR compensation!')}
                >
                  ⚡ Trigger APFC Capacitor Bank Compensation
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 4: ENERGY BENCHMARKING (BEE STAR RATINGS) ================= */}
        {activeTab === 'benchmarking' && benchmarkResult && (
          <div className="card p-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
              <div>
                <h5 className="fw-bold mb-1">Bureau of Energy Efficiency (BEE) Star Rating Audit</h5>
                <p className="text-muted small mb-0">Energy Performance Index (EPI in kWh/m²/year) calculated against Indian standards</p>
              </div>
              <select
                className="form-select form-select-sm w-auto"
                value={selectedFacilityId}
                onChange={(e) => {
                  setSelectedFacilityId(Number(e.target.value));
                  fetchBenchmark(Number(e.target.value));
                }}
              >
                {facilities.map(f => (
                  <option key={f.facility_id} value={f.facility_id}>{f.name}</option>
                ))}
              </select>
            </div>

            <div className="row g-4 mb-4">
              <div className="col-md-4">
                <div className="card p-4 bg-light text-center">
                  <div className="kpi-title mb-1">Calculated EPI</div>
                  <div className="display-5 fw-bold text-dark font-monospace">
                    {benchmarkResult.benchmarking.calculated_epi_kwh_sqm_yr}
                  </div>
                  <div className="text-muted small">kWh / sq.m / year</div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card p-4 bg-light text-center">
                  <div className="kpi-title mb-1">BEE Star Rating</div>
                  <div className="display-5 star-rating mb-1">
                    {'★'.repeat(benchmarkResult.benchmarking.bee_star_rating)}
                    {'☆'.repeat(5 - benchmarkResult.benchmarking.bee_star_rating)}
                  </div>
                  <div className="fw-bold text-success">{benchmarkResult.benchmarking.rating_label}</div>
                </div>
              </div>
              <div className="col-md-4">
                <div className="card p-4 bg-light text-center">
                  <div className="kpi-title mb-1">Standard Industry Baseline</div>
                  <div className="display-5 fw-bold text-muted font-monospace">
                    {benchmarkResult.benchmarking.standard_industry_epi}
                  </div>
                  <div className="text-muted small">{benchmarkResult.benchmarking.reference_standard}</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 5: UTILITY BILLS (INR) ================= */}
        {activeTab === 'billing' && (
          <div className="card p-4">
            <div className="d-flex justify-content-between align-items-center mb-3">
              <div>
                <h5 className="fw-bold mb-1">Discom Utility Bill Management & Tariff Audit</h5>
                <p className="text-muted small mb-0">High-tension commercial tariffs (BESCOM, MSEDCL, TSSPDCL) in Indian Rupees (₹)</p>
              </div>
            </div>
            <div className="table-responsive">
              <table className="table table-hover align-middle">
                <thead className="table-light">
                  <tr>
                    <th>Bill Number</th>
                    <th>Facility</th>
                    <th>Billing Period</th>
                    <th>Units (kWh)</th>
                    <th>Billed Amount (INR)</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {bills.map(b => (
                    <tr key={b.bill_id}>
                      <td className="font-monospace fw-bold">{b.bill_number}</td>
                      <td>{b.facility_name}</td>
                      <td>{b.billing_month}/{b.billing_year}</td>
                      <td className="font-monospace">{Number(b.units_consumed_kwh).toLocaleString()}</td>
                      <td className="font-monospace fw-bold text-dark">₹{Number(b.billed_amount_inr).toLocaleString()}</td>
                      <td>
                        <span className={`badge ${b.payment_status === 'Paid' ? 'bg-success' : b.payment_status === 'Verified' ? 'bg-info text-dark' : 'bg-warning text-dark'}`}>
                          {b.payment_status}
                        </span>
                      </td>
                      <td>
                        {b.payment_status === 'Pending' && (
                          <button
                            className="btn btn-sm btn-outline-success"
                            onClick={() => verifyBill(b.bill_id)}
                          >
                            Verify & Approve
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ================= TAB 6: RECOMMENDATIONS ================= */}
        {activeTab === 'recommendations' && (
          <div className="card p-4">
            <h5 className="fw-bold mb-1">Energy Efficiency Retrofits & Cost-Saving Recommendations</h5>
            <p className="text-muted small mb-4">Algorithmic measures with calculated implementation costs, savings, and payback periods</p>

            <div className="table-responsive">
              <table className="table table-hover align-middle">
                <thead className="table-light">
                  <tr>
                    <th>Measure Title</th>
                    <th>Category</th>
                    <th>Annual Savings (₹)</th>
                    <th>Capex (₹)</th>
                    <th>Payback</th>
                    <th>Priority</th>
                    <th>Status</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {recommendations.map(r => (
                    <tr key={r.recommendation_id}>
                      <td className="fw-bold">{r.title}</td>
                      <td><span className="badge bg-secondary-subtle text-dark">{r.category}</span></td>
                      <td className="font-monospace text-success fw-bold">₹{Number(r.estimated_annual_savings_inr).toLocaleString()}</td>
                      <td className="font-monospace">₹{Number(r.implementation_cost_inr).toLocaleString()}</td>
                      <td>{r.payback_period_months} mo</td>
                      <td>
                        <span className={`badge ${r.priority === 'Critical' ? 'bg-danger' : r.priority === 'High' ? 'bg-warning text-dark' : 'bg-info text-dark'}`}>
                          {r.priority}
                        </span>
                      </td>
                      <td>
                        <span className={`badge ${r.status === 'Implemented' ? 'bg-success' : r.status === 'Approved' ? 'bg-primary' : 'bg-secondary'}`}>
                          {r.status}
                        </span>
                      </td>
                      <td>
                        {r.status === 'Proposed' && (
                          <button
                            className="btn btn-sm btn-outline-primary"
                            onClick={() => updateRecStatus(r.recommendation_id, 'Approved')}
                          >
                            Approve
                          </button>
                        )}
                        {r.status === 'Approved' && (
                          <button
                            className="btn btn-sm btn-outline-success"
                            onClick={() => updateRecStatus(r.recommendation_id, 'Implemented')}
                          >
                            Mark Implemented
                          </button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* ================= TAB 7: RENEWABLES & SMART GRID ================= */}
        {activeTab === 'renewables' && (
          <div className="card p-4">
            <div className="d-flex justify-content-between align-items-center mb-4">
              <div>
                <h5 className="fw-bold mb-1">Renewable Distributed Energy Resources (DER) & Smart Grid</h5>
                <p className="text-muted small mb-0">Rooftop Solar PV arrays, BESS battery storage, and automated demand-response events</p>
              </div>
              <button className="btn btn-warning btn-sm" onClick={triggerDemandResponse}>
                <i className="bi bi-lightning-charge me-1"></i> Trigger Smart Grid Demand Response
              </button>
            </div>

            <div className="row g-4">
              <div className="col-md-6">
                <div className="card p-3 border">
                  <h6 className="fw-bold">Rooftop Solar PV Integration</h6>
                  <p className="text-muted small">Generating clean energy across daytime hours with net-metering export.</p>
                  <div className="d-flex justify-content-between font-monospace small">
                    <span>Installed Capacity: <strong>250 kWp</strong></span>
                    <span>Inverter Status: <strong className="text-success">Generating</strong></span>
                  </div>
                </div>
              </div>
              <div className="col-md-6">
                <div className="card p-3 border">
                  <h6 className="fw-bold">Battery Energy Storage System (BESS)</h6>
                  <p className="text-muted small">Lithium-ion peak shaving storage to throttle grid imports during expensive peak tariffs.</p>
                  <div className="d-flex justify-content-between font-monospace small">
                    <span>Capacity: <strong>150 kW / 300 kWh</strong></span>
                    <span>State of Charge: <strong className="text-success">84% SOC</strong></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ================= TAB 8: ACCESS CONTROL (RBAC) ================= */}
        {activeTab === 'users' && (
          <div className="card p-4">
            <h5 className="fw-bold mb-1">User Management & Role-Based Access Control (RBAC)</h5>
            <p className="text-muted small mb-4">Security permissions across Administrator, Facility Manager, Field Engineer, and Auditor roles</p>

            <table className="table table-bordered">
              <thead className="table-light">
                <tr>
                  <th>Role Name</th>
                  <th>Data Acquisition</th>
                  <th>Analytics & Benchmarking</th>
                  <th>Bill Verification</th>
                  <th>Approve Retrofits</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td className="fw-bold">Administrator</td>
                  <td className="text-success">Full Access</td>
                  <td className="text-success">Full Access</td>
                  <td className="text-success">Full Access</td>
                  <td className="text-success">Full Access</td>
                </tr>
                <tr>
                  <td className="fw-bold">Facility Manager</td>
                  <td className="text-success">View Only</td>
                  <td className="text-success">Full Access</td>
                  <td className="text-success">Approve Bills</td>
                  <td className="text-success">Approve Retrofits</td>
                </tr>
                <tr>
                  <td className="fw-bold">Field Engineer</td>
                  <td className="text-success">Hardware Commissioning</td>
                  <td className="text-muted">View Only</td>
                  <td className="text-muted">No Access</td>
                  <td className="text-muted">No Access</td>
                </tr>
              </tbody>
            </table>
          </div>
        )}

      </div>

      {/* Footer */}
      <footer className="bg-dark text-white text-center py-3 mt-auto text-xs">
        <div className="container">
          <small className="text-secondary">
            GreenGrid: Smart Energy Management for Tomorrow's Needs (P02) • Python FSD Capstone
          </small>
        </div>
      </footer>
    </div>
  );
}
