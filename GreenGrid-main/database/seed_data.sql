-- ============================================================================
-- GreenGrid: Smart Energy Management for Tomorrow's Needs
-- Realistic Indian Context Seed Data (2024 - 2026)
-- Cities: Bengaluru, Pune, Hyderabad, Mumbai, Gurugram, Chennai
-- Discoms: BESCOM, MSEDCL, TSSPDCL, TPDDL, TANGEDCO
-- Currencies: INR (₹)
-- ============================================================================

USE greengrid_db;

-- ----------------------------------------------------------------------------
-- 1. Insert Roles (Master)
-- ----------------------------------------------------------------------------
INSERT INTO roles (role_id, role_name, role_description) VALUES
(1, 'Administrator', 'System wide access, user governance, global benchmark definitions'),
(2, 'Facility Manager', 'Oversees energy budgets, billing approvals, and efficiency retrofits'),
(3, 'Field Engineer', 'Hardware meter commissioning, Modbus calibration, and sensor maintenance'),
(4, 'Energy Auditor', 'Conducts ISO 50001 compliance reviews and benchmarking assessments');

-- ----------------------------------------------------------------------------
-- 2. Insert Users (Admin + Business Roles with hashed password placeholders)
-- Hashed password for demo: pbkdf2_sha256$600000$GreenGridSalt$HashDemo...
-- ----------------------------------------------------------------------------
INSERT INTO users (user_id, username, email, password_hash, full_name, phone_number, role_id, is_active) VALUES
(1, 'admin_greengrid', 'admin@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Rajesh K. Sharma', '+91-9811223344', 1, 1),
(2, 'mgr_arun_bengaluru', 'arun.nair@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Arun V. Nair', '+91-9845012345', 2, 1),
(3, 'mgr_priya_pune', 'priya.deshmukh@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Priya Deshmukh', '+91-9822098765', 2, 1),
(4, 'mgr_vikram_hyderabad', 'vikram.reddy@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Vikramaditya Reddy', '+91-9988776655', 2, 1),
(5, 'eng_sanjay_field', 'sanjay.patel@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Sanjay Patel', '+91-9711224466', 3, 1),
(6, 'eng_deepak_field', 'deepak.verma@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Deepak Verma', '+91-9899001122', 3, 1),
(7, 'auditor_ananya', 'ananya.sen@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Ananya Sengupta', '+91-9833445566', 4, 1),
(8, 'mgr_amit_delhi', 'amit.khanna@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Amit Khanna', '+91-9810123456', 2, 1),
(9, 'mgr_karthik_chennai', 'karthik.subramanian@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Karthik Subramanian', '+91-9444012345', 2, 1),
(10, 'eng_neha_iot', 'neha.kulkarni@greengrid.in', 'pbkdf2_sha256$600000$demo$7e1a3b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6', 'Neha Kulkarni', '+91-9765432109', 3, 1),
-- Edge Case User 1: Missing phone number (optional field test)
(11, 'user_guest_test', 'guest.test@greengrid.in', 'pbkdf2_sha256$600000$demo$placeholder', 'Guest Auditor', NULL, 4, 0),
-- Edge Case User 2: Duplicate-looking name variations
(12, 'rajesh_sharma_jr', 'rajesh.sharma.jr@greengrid.in', 'pbkdf2_sha256$600000$demo$placeholder', 'Rajesh K. Sharma Jr', '+91-9811223399', 3, 1);

-- ----------------------------------------------------------------------------
-- 3. Insert Facilities (Master)
-- ----------------------------------------------------------------------------
INSERT INTO facilities (facility_id, facility_code, name, facility_type, address, city, state, pincode, total_area_sqft, built_year, manager_id, baseline_kwh_per_sqm) VALUES
(1, 'BLR-FAC-01', 'Manyata Tech Park Tower 7', 'IT Park', 'Outer Ring Road, Nagavara', 'Bengaluru', 'Karnataka', '560045', 250000.00, 2018, 2, 142.50),
(2, 'BLR-FAC-02', 'Electronic City Campus B', 'IT Park', 'Phase 1, Hosur Road', 'Bengaluru', 'Karnataka', '560100', 180000.00, 2016, 2, 138.00),
(3, 'PUN-FAC-01', 'Hinjawadi Infotech Zone 3', 'IT Park', 'Phase 2, Hinjawadi', 'Pune', 'Maharashtra', '411057', 310000.00, 2019, 3, 155.00),
(4, 'PUN-FAC-02', 'Chakan Auto Components Plant', 'Manufacturing Plant', 'MIDC Phase II, Chakan', 'Pune', 'Maharashtra', '410501', 145000.00, 2015, 3, 260.00),
(5, 'HYD-FAC-01', 'HITEC City Cyber Gateways', 'Commercial Office', 'Madhapur', 'Hyderabad', 'Telangana', '500081', 220000.00, 2020, 4, 132.00),
(6, 'HYD-FAC-02', 'Genome Valley BioPharma Lab', 'Manufacturing Plant', 'Shamirpet', 'Hyderabad', 'Telangana', '500078', 95000.00, 2021, 4, 310.00),
(7, 'DEL-FAC-01', 'CyberHub Corporate Suites', 'Commercial Office', 'DLF Cyber City, Phase 2', 'Gurugram', 'Haryana', '122002', 190000.00, 2017, 8, 168.00),
(8, 'CHN-FAC-01', 'OMR Tech Corridor Hub', 'IT Park', 'Rajiv Gandhi Salai, Thoraipakkam', 'Chennai', 'Tamil Nadu', '600097', 280000.00, 2019, 9, 145.00),
(9, 'MUM-FAC-01', 'BKC Financial Center West', 'Commercial Office', 'Bandra Kurla Complex', 'Mumbai', 'Maharashtra', '400051', 340000.00, 2018, 3, 175.00),
(10, 'BLR-FAC-03', 'Whitefield Eco-Care Hospital', 'Hospital', 'ITPL Main Road, Whitefield', 'Bengaluru', 'Karnataka', '560066', 160000.00, 2020, 2, 285.00),
-- Edge Case Facility 1: Maximum length name boundary test
(11, 'EDG-FAC-01', 'Sardar Vallabhbhai Patel Integrated CleanTech Renewable Science Research and High Performance Supercomputing Center of Excellence', 'Educational Campus', 'Knowledge City Boulevard', 'Bengaluru', 'Karnataka', '560099', 500000.00, 2023, 2, 110.00),
-- Edge Case Facility 2: Very small area boundary test
(12, 'EDG-FAC-02', 'Mini Modular Edge Data Center', 'Commercial Office', 'MIDC Micro Park', 'Pune', 'Maharashtra', '411014', 1200.00, 2024, 3, 450.00);

-- ----------------------------------------------------------------------------
-- 4. Insert Benchmarks (BEE Standards)
-- ----------------------------------------------------------------------------
INSERT INTO benchmarks (benchmark_id, facility_type, climate_zone, benchmark_name, standard_epi_kwh_sqm_yr, bee_star_1_max, bee_star_2_max, bee_star_3_max, bee_star_4_max, bee_star_5_max) VALUES
(1, 'IT Park', 'Moderate', 'BEE Commercial Buildings - Moderate Zone', 140.00, 200.00, 175.00, 150.00, 125.00, 100.00),
(2, 'Commercial Office', 'Composite', 'BEE Office Buildings - Composite Zone', 160.00, 220.00, 190.00, 165.00, 135.00, 110.00),
(3, 'Hospital', 'Warm and Humid', 'BEE Healthcare Star Rating Standard', 275.00, 380.00, 340.00, 300.00, 260.00, 220.00),
(4, 'Manufacturing Plant', 'Hot and Dry', 'Industrial Energy Efficiency Guideline', 250.00, 350.00, 310.00, 270.00, 230.00, 190.00),
(5, 'Educational Campus', 'Moderate', 'Institutional Green Campus Standard', 90.00, 140.00, 120.00, 100.00, 80.00, 60.00),
(6, 'Retail Mall', 'Composite', 'Retail & Commercial Center Standard', 220.00, 300.00, 270.00, 240.00, 200.00, 160.00);

-- ----------------------------------------------------------------------------
-- 5. Insert Utility Providers (Discoms)
-- ----------------------------------------------------------------------------
INSERT INTO utility_providers (provider_id, provider_name, state, tariff_code, customer_care_no, discom_type) VALUES
(1, 'Bangalore Electricity Supply Company (BESCOM)', 'Karnataka', 'HT-2(a) Commercial', '1912', 'State Discom'),
(2, 'Maharashtra State Electricity Distribution Co (MSEDCL)', 'Maharashtra', 'HT-I Industrial & Commercial', '1800-233-3435', 'State Discom'),
(3, 'Telangana Southern Power Distribution Co (TSSPDCL)', 'Telangana', 'HT Category-II', '1912', 'State Discom'),
(4, 'Tata Power Delhi Distribution Limited (TPDDL)', 'Delhi', 'ND-HT Commercial', '19124', 'Private Discom'),
(5, 'Tamil Nadu Generation and Distribution Corp (TANGEDCO)', 'Tamil Nadu', 'HT Tariff III', '94987-94987', 'State Discom'),
(6, 'Adani Electricity Mumbai Limited (AEML)', 'Maharashtra', 'HT-Commercial-BKC', '19122', 'Private Discom');

-- ----------------------------------------------------------------------------
-- 6. Insert Meters
-- ----------------------------------------------------------------------------
INSERT INTO meters (meter_id, meter_serial_no, facility_id, meter_name, meter_type, manufacturer, model, installation_date, status, ip_address, modbus_slave_id) VALUES
(1, 'SCH-MTR-BLR-001', 1, 'Manyata Main Grid Incomer Feeder', 'Main Incomer', 'Schneider Electric', 'PowerLogic ION9000', '2023-01-15', 'Active', '192.168.10.21', 1),
(2, 'SCH-MTR-BLR-002', 1, 'Manyata Central Chiller Plant 1', 'HVAC Feeder', 'Schneider Electric', 'PM8000', '2023-01-16', 'Active', '192.168.10.22', 2),
(3, 'ABB-MTR-BLR-003', 1, 'Manyata Server Room UPS Bus A', 'UPS & Data Center', 'ABB', 'M4M 30 Modbus', '2023-02-10', 'Active', '192.168.10.23', 3),
(4, 'SCH-MTR-BLR-004', 1, 'Manyata Rooftop 250kW Solar Feeder', 'Solar Inverter Feed', 'Schneider Electric', 'PM5560', '2023-03-01', 'Active', '192.168.10.24', 4),
(5, 'LNT-MTR-ECI-001', 2, 'ECity Campus Main Transformer', 'Main Incomer', 'L&T Electrical', 'Quasar Multifunction', '2022-11-20', 'Active', '192.168.11.10', 1),
(6, 'LNT-MTR-ECI-002', 2, 'ECity AHU & Air Ventilation Subsystem', 'HVAC Feeder', 'L&T Electrical', 'Acuvim II', '2022-11-20', 'Active', '192.168.11.11', 2),
(7, 'SCH-MTR-PUN-001', 3, 'Hinjawadi Zone 3 Primary Feeder', 'Main Incomer', 'Schneider Electric', 'ION9000', '2023-04-12', 'Active', '192.168.20.15', 1),
(8, 'YOK-MTR-PUN-002', 4, 'Chakan Heavy CNC Foundry Machine Bus', 'Industrial Machinery', 'Yokogawa', 'CW500', '2022-08-14', 'Warning', '192.168.21.30', 2),
(9, 'SIE-MTR-HYD-001', 5, 'HITEC CyberGateways Incomer', 'Main Incomer', 'Siemens', 'PAC4200', '2023-06-05', 'Active', '192.168.30.12', 1),
(10, 'SIE-MTR-HYD-002', 6, 'Genome BioPharma Cleanroom HVAC', 'HVAC Feeder', 'Siemens', 'PAC3200', '2023-07-20', 'Active', '192.168.31.18', 2),
(11, 'SCH-MTR-DEL-001', 7, 'CyberHub Corporate Main Feed', 'Main Incomer', 'Schneider Electric', 'ION9000', '2023-02-18', 'Active', '192.168.40.10', 1),
(12, 'LNT-MTR-CHN-001', 8, 'OMR Corridor Incomer A', 'Main Incomer', 'L&T Electrical', 'Quasar', '2023-05-14', 'Active', '192.168.50.11', 1),
(13, 'ABB-MTR-MUM-001', 9, 'BKC Financial Center High Voltage Feed', 'Main Incomer', 'ABB', 'M4M 30', '2023-01-28', 'Active', '192.168.60.10', 1),
(14, 'SCH-MTR-BLR-005', 10, 'Whitefield Hospital ICU & OT Supply', 'UPS & Data Center', 'Schneider Electric', 'PM8000', '2023-09-01', 'Active', '192.168.12.14', 1),
-- Edge Case Meter: Meter with NULL IP & Offline status
(15, 'EDG-MTR-OFF-999', 11, 'Knowledge City Decommissioned Backup Feed', 'Lighting', 'Conzerve', 'EM6400', '2024-01-10', 'Offline', NULL, NULL);

-- ----------------------------------------------------------------------------
-- 7. Insert Telemetry Readings (Sample Slice)
-- ----------------------------------------------------------------------------
INSERT INTO telemetry_readings (reading_id, meter_id, reading_timestamp, active_power_kw, reactive_power_kvar, voltage_v, current_a, power_factor, frequency_hz, cumulative_energy_kwh) VALUES
(1, 1, '2026-11-20 00:00:00', 380.50, 112.40, 415.2, 545.2, 0.958, 50.02, 1284500.50),
(2, 1, '2026-11-20 01:00:00', 340.20, 105.10, 415.8, 488.1, 0.955, 49.98, 1284840.70),
(3, 1, '2026-11-20 02:00:00', 320.00, 98.60, 416.1, 458.7, 0.956, 50.01, 1285160.70),
(4, 1, '2026-11-20 03:00:00', 315.40, 96.00, 416.5, 451.6, 0.957, 50.04, 1285476.10),
(5, 1, '2026-11-20 04:00:00', 330.10, 102.30, 415.9, 473.2, 0.955, 50.03, 1285806.20),
(6, 1, '2026-11-20 05:00:00', 390.80, 120.50, 415.0, 560.4, 0.956, 49.97, 1286197.00),
(7, 1, '2026-11-20 06:00:00', 510.60, 158.20, 414.2, 734.2, 0.955, 49.95, 1286707.60),
(8, 1, '2026-11-20 07:00:00', 680.00, 210.40, 413.5, 980.5, 0.955, 49.94, 1287387.60),
(9, 1, '2026-11-20 08:00:00', 890.50, 280.10, 412.8, 1288.0, 0.954, 49.92, 1288278.10),
(10, 1, '2026-11-20 09:00:00', 1120.40, 360.20, 411.9, 1625.5, 0.952, 49.90, 1289398.50),
(11, 1, '2026-11-20 10:00:00', 1250.00, 410.00, 411.2, 1818.2, 0.950, 49.88, 1290648.50),
(12, 1, '2026-11-20 11:00:00', 1320.80, 440.60, 410.8, 1925.8, 0.949, 49.86, 1291969.30),
(13, 1, '2026-11-20 12:00:00', 1380.00, 465.00, 410.5, 2014.6, 0.948, 49.85, 1293349.30),
(14, 1, '2026-11-20 13:00:00', 1290.50, 430.00, 411.0, 1881.0, 0.949, 49.87, 1294639.80),
(15, 1, '2026-11-20 14:00:00', 1395.20, 475.00, 410.2, 2039.5, 0.947, 49.84, 1296035.00),
(16, 1, '2026-11-20 15:00:00', 1340.00, 450.00, 410.7, 1956.1, 0.948, 49.86, 1297375.00),
(17, 1, '2026-11-20 16:00:00', 1260.40, 418.00, 411.3, 1836.5, 0.950, 49.89, 1298635.40),
(18, 1, '2026-11-20 17:00:00', 1150.00, 375.00, 412.0, 1671.0, 0.951, 49.91, 1299785.40),
(19, 1, '2026-11-20 18:00:00', 980.20, 310.50, 412.8, 1420.4, 0.953, 49.93, 1300765.60),
(20, 1, '2026-11-20 19:00:00', 820.00, 255.00, 413.6, 1185.0, 0.955, 49.96, 1301585.60),
(21, 1, '2026-11-20 20:00:00', 690.40, 212.00, 414.2, 995.1, 0.956, 49.98, 1302276.00),
(22, 1, '2026-11-20 21:00:00', 580.00, 178.00, 414.9, 834.0, 0.956, 50.00, 1302856.00),
(23, 1, '2026-11-20 22:00:00', 490.50, 150.00, 415.3, 703.8, 0.956, 50.02, 1303346.50),
(24, 1, '2026-11-20 23:00:00', 410.00, 125.00, 415.7, 587.2, 0.957, 50.03, 1303756.50),
-- Meter 4: Solar Generation Readings (Peak at Noon)
(25, 4, '2026-11-20 06:00:00', 0.00, 0.00, 415.0, 0.0, 1.000, 50.00, 185200.00),
(26, 4, '2026-11-20 09:00:00', 115.40, 5.20, 415.2, 160.8, 0.999, 49.98, 185315.40),
(27, 4, '2026-11-20 12:00:00', 242.80, 8.10, 415.5, 338.2, 0.999, 49.96, 185790.00),
(28, 4, '2026-11-20 15:00:00', 165.20, 6.40, 415.1, 230.1, 0.999, 49.97, 186250.00),
(29, 4, '2026-11-20 18:00:00', 12.00, 1.00, 415.0, 16.7, 0.997, 49.99, 186350.00),
-- Edge Case Reading: Poor Power Factor (0.842) triggering reactive penalty warning
(30, 8, '2026-11-20 14:30:00', 580.00, 375.00, 408.0, 978.0, 0.842, 49.80, 894500.00);

-- ----------------------------------------------------------------------------
-- 8. Insert Utility Bills
-- ----------------------------------------------------------------------------
INSERT INTO utility_bills (bill_id, facility_id, provider_id, consumer_account_no, bill_number, billing_month, billing_year, units_consumed_kwh, peak_units_kwh, off_peak_units_kwh, billed_amount_inr, tariff_rate_inr_kwh, penalty_inr, due_date, payment_status, verified_by) VALUES
(1, 1, 1, 'BES-CA-9041284', 'BESCOM-2026-OCT-0941', 10, 2026, 482500.00, 168000.00, 314500.00, 4101250.00, 8.50, 0.00, '2026-11-15', 'Paid', 2),
(2, 1, 1, 'BES-CA-9041284', 'BESCOM-2026-SEP-0812', 9, 2026, 496000.00, 175000.00, 321000.00, 4216000.00, 8.50, 0.00, '2026-10-15', 'Paid', 2),
(3, 2, 1, 'BES-CA-8812301', 'BESCOM-2026-OCT-1102', 10, 2026, 310000.00, 105000.00, 205000.00, 2635000.00, 8.50, 0.00, '2026-11-18', 'Verified', 2),
(4, 3, 2, 'MSE-CA-4491023', 'MSEDCL-2026-OCT-7721', 10, 2026, 620000.00, 230000.00, 390000.00, 5890000.00, 9.50, 0.00, '2026-11-20', 'Pending', 3),
(5, 4, 2, 'MSE-CA-1120492', 'MSEDCL-2026-OCT-8819', 10, 2026, 410000.00, 160000.00, 250000.00, 4018000.00, 9.80, 15400.00, '2026-11-22', 'Pending', 3),
(6, 5, 3, 'TSS-CA-5582910', 'TSSPDCL-2026-OCT-3401', 10, 2026, 390000.00, 135000.00, 255000.00, 3432000.00, 8.80, 0.00, '2026-11-14', 'Paid', 4),
(7, 7, 4, 'TPD-CA-7719283', 'TPDDL-2026-OCT-5509', 10, 2026, 430000.00, 160000.00, 270000.00, 4085000.00, 9.50, 0.00, '2026-11-12', 'Paid', 8),
(8, 8, 5, 'TAN-CA-6619204', 'TANGEDCO-2026-OCT-1092', 10, 2026, 510000.00, 185000.00, 325000.00, 4335000.00, 8.50, 0.00, '2026-11-16', 'Paid', 9),
(9, 9, 6, 'AEM-CA-3329102', 'AEML-2026-OCT-6612', 10, 2026, 680000.00, 260000.00, 420000.00, 7140000.00, 10.50, 0.00, '2026-11-19', 'Verified', 3),
(10, 10, 1, 'BES-CA-9920194', 'BESCOM-2026-OCT-4410', 10, 2026, 375000.00, 140000.00, 235000.00, 3187500.00, 8.50, 0.00, '2026-11-15', 'Paid', 2),
-- Edge Case Bill: Disputed bill with penalty
(11, 4, 2, 'MSE-CA-1120492', 'MSEDCL-2026-SEP-8818', 9, 2026, 435000.00, 180000.00, 255000.00, 4350000.00, 10.00, 45000.00, '2026-10-22', 'Disputed', 3);

-- ----------------------------------------------------------------------------
-- 9. Insert Energy Efficiency Recommendations
-- ----------------------------------------------------------------------------
INSERT INTO recommendations (recommendation_id, facility_id, title, category, description, estimated_annual_savings_inr, estimated_kwh_savings, implementation_cost_inr, payback_period_months, status, priority) VALUES
(1, 1, 'VFD Retrofit on Central Chiller Condenser Pumps', 'HVAC Optimization', 'Install Variable Frequency Drives on 3x 75kW condenser water pumps to dynamically adjust flow rate based on outdoor wet-bulb temperature.', 850000.00, 100000.00, 1200000.00, 16.9, 'Approved', 'High'),
(2, 1, 'Automatic Capacitor Bank PF Correction', 'Power Factor Correction', 'Deploy 150 kVAR switched APFC capacitor banks to raise plant average power factor from 0.948 to 0.995, eliminating Discom low-PF penalty surcharge.', 420000.00, 45000.00, 380000.00, 10.8, 'Implemented', 'Critical'),
(3, 2, 'Basement Parking Smart Motion Sensor LED Retrofit', 'Lighting Retrofit', 'Replace 650 conventional 36W fluorescent tubes with 14W occupancy-sensing microwave radar LED fixtures.', 280000.00, 33000.00, 210000.00, 9.0, 'Implemented', 'Medium'),
(4, 3, 'Pre-Cooling Thermal Storage & Peak Shaving', 'Peak Shaving', 'Utilize building chilled water storage to pre-cool facility between 04:00 - 06:00 during off-peak tariff (₹5.5/kWh) and throttle chillers during 14:00 - 18:00 peak hours (₹12.0/kWh).', 1450000.00, 140000.00, 1800000.00, 14.9, 'Proposed', 'High'),
(5, 5, 'Rooftop Solar PV Expansion by 180 kWp', 'Solar Expansion', 'Expand existing 120 kWp solar PV array utilizing unoccupied cafeteria terrace to generate an additional 250,000 kWh annually.', 1950000.00, 250000.00, 6800000.00, 41.8, 'Under Review', 'Medium'),
(6, 4, 'Compressed Air Leakage Audit and Auto-Shutoff Valves', 'HVAC Optimization', 'Eliminate ultrasonic leaks across manufacturing pneumatic lines and install automated solenoid isolation valves during non-production shifts.', 620000.00, 65000.00, 320000.00, 6.2, 'Approved', 'High'),
(7, 8, 'Data Center Hot/Cold Aisle Containment Barriers', 'HVAC Optimization', 'Install physical modular vinyl blanking panels and hot aisle containment to increase CRAC return air temperature and lower chiller lift.', 780000.00, 92000.00, 650000.00, 10.0, 'Proposed', 'Medium'),
(8, 7, 'After-Hours Phantom Load Automatic Power Strips', 'Behavioral', 'Implement IoT scheduled smart power sockets to isolate idle workstation monitors, printers, and water dispensers between 21:00 and 07:00.', 190000.00, 20000.00, 120000.00, 7.6, 'Approved', 'Low'),
-- Edge Case Recommendation: Zero implementation cost behavioral measure
(9, 2, 'Workplace Summer Thermostat Setpoint Realignment (24°C to 26°C)', 'Behavioral', 'Adopt Bureau of Energy Efficiency standard 24-26°C comfort range, reducing compressor duty cycles by 6% without capital expenditure.', 340000.00, 40000.00, 0.00, 0.0, 'Implemented', 'High');

-- ----------------------------------------------------------------------------
-- 10. Insert Renewable Systems (DERs)
-- ----------------------------------------------------------------------------
INSERT INTO renewable_systems (system_id, facility_id, system_type, capacity_kw, installation_date, inverter_model, azimuth_angle, tilt_angle, status) VALUES
(1, 1, 'Rooftop Solar PV', 250.00, '2023-02-15', 'SMA Sunny Tripower CORE2 110kW', 180.0, 15.0, 'Generating'),
(2, 1, 'Battery Storage (BESS)', 150.00, '2023-04-20', 'Tesla Megapack Commercial Li-Ion', 0.0, 0.0, 'Generating'),
(3, 2, 'Rooftop Solar PV', 180.00, '2022-10-10', 'Huawei SUN2000-100KTL', 180.0, 14.5, 'Generating'),
(4, 3, 'Rooftop Solar PV', 320.00, '2023-05-18', 'Fimer PVS-100/120', 180.0, 18.0, 'Generating'),
(5, 4, 'Wind Turbine', 200.00, '2021-12-05', 'Suzlon S111 Small Wind Hub', 240.0, 0.0, 'Generating'),
(6, 5, 'Rooftop Solar PV', 120.00, '2023-08-22', 'Delta M70A Inverter', 180.0, 16.0, 'Generating'),
(7, 8, 'Hybrid Solar-Wind', 280.00, '2023-06-30', 'Sungrow SG110CX Hybrid', 180.0, 15.0, 'Generating'),
(8, 9, 'Battery Storage (BESS)', 250.00, '2023-09-12', 'Fluence Energy GridStack 500kWh', 0.0, 0.0, 'Generating');

-- ----------------------------------------------------------------------------
-- 11. Insert Renewable Generation Logs
-- ----------------------------------------------------------------------------
INSERT INTO renewable_generation_logs (log_id, system_id, log_timestamp, generation_kwh, battery_charge_kwh, battery_discharge_kwh, grid_export_kwh, grid_import_kwh, battery_soc_percent) VALUES
(1, 1, '2026-11-20 08:00:00', 45.00, 10.00, 0.00, 0.00, 845.00, 45.00),
(2, 1, '2026-11-20 09:00:00', 115.00, 25.00, 0.00, 0.00, 1005.00, 52.00),
(3, 1, '2026-11-20 10:00:00', 180.00, 40.00, 0.00, 0.00, 1070.00, 64.00),
(4, 1, '2026-11-20 11:00:00', 225.00, 45.00, 0.00, 0.00, 1095.00, 78.00),
(5, 1, '2026-11-20 12:00:00', 248.00, 30.00, 0.00, 15.00, 1132.00, 88.00),
(6, 1, '2026-11-20 13:00:00', 242.00, 20.00, 0.00, 10.00, 1048.00, 94.00),
(7, 1, '2026-11-20 14:00:00', 215.00, 0.00, 80.00, 0.00, 1100.00, 84.00),
(8, 1, '2026-11-20 15:00:00', 165.00, 0.00, 80.00, 0.00, 1095.00, 72.00),
(9, 1, '2026-11-20 16:00:00', 105.00, 0.00, 80.00, 0.00, 1075.00, 60.00),
(10, 1, '2026-11-20 17:00:00', 42.00, 0.00, 50.00, 0.00, 1058.00, 52.00);

-- ----------------------------------------------------------------------------
-- 12. Insert Demand Response Events
-- ----------------------------------------------------------------------------
INSERT INTO demand_response_events (event_id, facility_id, event_title, target_shed_kw, actual_shed_kw, start_time, end_time, incentive_earned_inr, status) VALUES
(1, 1, 'BESCOM Summer Peak Clipping DR Program', 200.00, 215.50, '2026-11-18 14:00:00', '2026-11-18 16:00:00', 25000.00, 'Completed'),
(2, 3, 'MSEDCL Grid Emergency Load Relief', 250.00, 240.00, '2026-11-15 18:00:00', '2026-11-15 20:00:00', 32000.00, 'Completed'),
(3, 4, 'Chakan Industrial Feeder Peak Shifting', 150.00, 162.00, '2026-11-19 13:00:00', '2026-11-19 15:00:00', 18500.00, 'Completed'),
(4, 5, 'TSSPDCL Smart City Microgrid Balancing Call', 180.00, 0.00, '2026-11-25 15:00:00', '2026-11-25 17:00:00', 0.00, 'Scheduled');
