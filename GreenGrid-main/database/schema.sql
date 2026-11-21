-- ============================================================================
-- GreenGrid: Smart Energy Management for Tomorrow's Needs
-- Database: MySQL 8.0 (InnoDB, utf8mb4)
-- Normalization: Third Normal Form (3NF)
-- Modules Covered:
--   1. Data Acquisition & Integration
--   2. Energy Analytics
--   3. Visualization & Dashboard
--   4. Energy Benchmarking
--   5. Utility Bill Management
--   6. Energy Efficiency Recommendations
--   7. Renewable Energy & Smart Grid Integration
--   8. User Management & Access Control
-- ============================================================================

CREATE DATABASE IF NOT EXISTS greengrid_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE greengrid_db;

-- ----------------------------------------------------------------------------
-- Table 1: roles (Master table for Access Control)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 2: users (User accounts with hashed passwords)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    phone_number VARCHAR(15) NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    last_login TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_users_role FOREIGN KEY (role_id) REFERENCES roles(role_id) ON DELETE RESTRICT,
    INDEX idx_users_email (email),
    INDEX idx_users_role (role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 3: facilities (Master table of commercial/industrial facilities)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS facilities (
    facility_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_code VARCHAR(30) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    facility_type ENUM('Commercial Office', 'IT Park', 'Manufacturing Plant', 'Hospital', 'Educational Campus', 'Retail Mall') NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    total_area_sqft DECIMAL(12, 2) NOT NULL,
    built_year INT NOT NULL,
    manager_id INT NULL,
    baseline_kwh_per_sqm DECIMAL(8, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_facilities_manager FOREIGN KEY (manager_id) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_facilities_city (city),
    INDEX idx_facilities_type (facility_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 4: meters (Hardware smart energy meters / BMS data acquisition units)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS meters (
    meter_id INT AUTO_INCREMENT PRIMARY KEY,
    meter_serial_no VARCHAR(60) NOT NULL UNIQUE,
    facility_id INT NOT NULL,
    meter_name VARCHAR(150) NOT NULL,
    meter_type ENUM('Main Incomer', 'HVAC Feeder', 'Lighting', 'UPS & Data Center', 'Industrial Machinery', 'Solar Inverter Feed') NOT NULL,
    manufacturer VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    installation_date DATE NOT NULL,
    status ENUM('Active', 'Warning', 'Fault', 'Offline') DEFAULT 'Active',
    ip_address VARCHAR(45) NULL,
    modbus_slave_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_meters_facility FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE,
    INDEX idx_meters_facility (facility_id),
    INDEX idx_meters_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 5: telemetry_readings (High-frequency time-series energy consumption data)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS telemetry_readings (
    reading_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    meter_id INT NOT NULL,
    reading_timestamp DATETIME NOT NULL,
    active_power_kw DECIMAL(10, 3) NOT NULL,
    reactive_power_kvar DECIMAL(10, 3) NOT NULL,
    voltage_v DECIMAL(6, 2) NOT NULL,
    current_a DECIMAL(8, 2) NOT NULL,
    power_factor DECIMAL(4, 3) NOT NULL,
    frequency_hz DECIMAL(5, 2) NOT NULL DEFAULT 50.00,
    cumulative_energy_kwh DECIMAL(14, 3) NOT NULL,
    recorded_by VARCHAR(50) DEFAULT 'MODBUS_GATEWAY',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_telemetry_meter FOREIGN KEY (meter_id) REFERENCES meters(meter_id) ON DELETE CASCADE,
    INDEX idx_telemetry_timestamp (reading_timestamp),
    INDEX idx_telemetry_meter_time (meter_id, reading_timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 6: benchmarks (Industry benchmarks e.g., BEE India star rating standards)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS benchmarks (
    benchmark_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_type VARCHAR(100) NOT NULL,
    climate_zone ENUM('Warm and Humid', 'Composite', 'Hot and Dry', 'Moderate', 'Cold') NOT NULL,
    benchmark_name VARCHAR(150) NOT NULL,
    standard_epi_kwh_sqm_yr DECIMAL(8, 2) NOT NULL,
    bee_star_1_max DECIMAL(8, 2) NOT NULL,
    bee_star_2_max DECIMAL(8, 2) NOT NULL,
    bee_star_3_max DECIMAL(8, 2) NOT NULL,
    bee_star_4_max DECIMAL(8, 2) NOT NULL,
    bee_star_5_max DECIMAL(8, 2) NOT NULL,
    reference_standard VARCHAR(100) DEFAULT 'BEE Energy Conservation Code',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_benchmarks_type_zone (facility_type, climate_zone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 7: utility_providers (Discom electricity distribution companies)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS utility_providers (
    provider_id INT AUTO_INCREMENT PRIMARY KEY,
    provider_name VARCHAR(150) NOT NULL UNIQUE,
    state VARCHAR(100) NOT NULL,
    tariff_code VARCHAR(50) NOT NULL,
    customer_care_no VARCHAR(20) NULL,
    discom_type ENUM('State Discom', 'Private Discom', 'Municipal Body') DEFAULT 'State Discom',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 8: utility_bills (Monthly Discom utility billing audit & management)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS utility_bills (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_id INT NOT NULL,
    provider_id INT NOT NULL,
    consumer_account_no VARCHAR(50) NOT NULL,
    bill_number VARCHAR(80) NOT NULL UNIQUE,
    billing_month INT NOT NULL,
    billing_year INT NOT NULL,
    units_consumed_kwh DECIMAL(12, 2) NOT NULL,
    peak_units_kwh DECIMAL(12, 2) NOT NULL,
    off_peak_units_kwh DECIMAL(12, 2) NOT NULL,
    billed_amount_inr DECIMAL(12, 2) NOT NULL,
    tariff_rate_inr_kwh DECIMAL(6, 2) NOT NULL,
    penalty_inr DECIMAL(10, 2) DEFAULT 0.00,
    due_date DATE NOT NULL,
    payment_status ENUM('Pending', 'Verified', 'Paid', 'Disputed') DEFAULT 'Pending',
    verified_by INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_bills_facility FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE RESTRICT,
    CONSTRAINT fk_bills_provider FOREIGN KEY (provider_id) REFERENCES utility_providers(provider_id) ON DELETE RESTRICT,
    CONSTRAINT fk_bills_verifier FOREIGN KEY (verified_by) REFERENCES users(user_id) ON DELETE SET NULL,
    INDEX idx_bills_facility (facility_id),
    INDEX idx_bills_year_month (billing_year, billing_month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 9: recommendations (AI & algorithmic energy efficiency measures)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    category ENUM('HVAC Optimization', 'Lighting Retrofit', 'Peak Shaving', 'Power Factor Correction', 'Solar Expansion', 'Behavioral') NOT NULL,
    description TEXT NOT NULL,
    estimated_annual_savings_inr DECIMAL(12, 2) NOT NULL,
    estimated_kwh_savings DECIMAL(12, 2) NOT NULL,
    implementation_cost_inr DECIMAL(12, 2) NOT NULL,
    payback_period_months DECIMAL(5, 1) NOT NULL,
    status ENUM('Proposed', 'Under Review', 'Approved', 'Implemented', 'Rejected') DEFAULT 'Proposed',
    priority ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_recs_facility FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE,
    INDEX idx_recs_facility (facility_id),
    INDEX idx_recs_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 10: renewable_systems (On-site Distributed Energy Resources)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS renewable_systems (
    system_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_id INT NOT NULL,
    system_type ENUM('Rooftop Solar PV', 'Wind Turbine', 'Battery Storage (BESS)', 'Hybrid Solar-Wind') NOT NULL,
    capacity_kw DECIMAL(10, 2) NOT NULL,
    installation_date DATE NOT NULL,
    inverter_model VARCHAR(100) NOT NULL,
    tilt_angle DECIMAL(4, 1) DEFAULT 15.0,
    azimuth_angle DECIMAL(5, 1) DEFAULT 180.0,
    status ENUM('Generating', 'Standby', 'Maintenance', 'Fault') DEFAULT 'Generating',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_renewables_facility FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE,
    INDEX idx_renewables_facility (facility_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 11: renewable_generation_logs (Solar/Wind telemetry & Net Metering)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS renewable_generation_logs (
    log_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    system_id INT NOT NULL,
    log_timestamp DATETIME NOT NULL,
    generation_kwh DECIMAL(10, 2) NOT NULL,
    battery_charge_kwh DECIMAL(10, 2) DEFAULT 0.00,
    battery_discharge_kwh DECIMAL(10, 2) DEFAULT 0.00,
    grid_export_kwh DECIMAL(10, 2) DEFAULT 0.00,
    grid_import_kwh DECIMAL(10, 2) DEFAULT 0.00,
    battery_soc_percent DECIMAL(5, 2) DEFAULT 80.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_renlogs_system FOREIGN KEY (system_id) REFERENCES renewable_systems(system_id) ON DELETE CASCADE,
    INDEX idx_renlogs_timestamp (log_timestamp),
    INDEX idx_renlogs_system (system_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ----------------------------------------------------------------------------
-- Table 12: demand_response_events (Smart Grid Demand-Response Programs)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS demand_response_events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    facility_id INT NOT NULL,
    event_title VARCHAR(150) NOT NULL,
    target_shed_kw DECIMAL(10, 2) NOT NULL,
    actual_shed_kw DECIMAL(10, 2) DEFAULT 0.00,
    start_time DATETIME NOT NULL,
    end_time DATETIME NOT NULL,
    incentive_earned_inr DECIMAL(10, 2) DEFAULT 0.00,
    status ENUM('Scheduled', 'In Progress', 'Completed', 'Cancelled') DEFAULT 'Scheduled',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_drevents_facility FOREIGN KEY (facility_id) REFERENCES facilities(facility_id) ON DELETE CASCADE,
    INDEX idx_drevents_facility (facility_id),
    INDEX idx_drevents_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
