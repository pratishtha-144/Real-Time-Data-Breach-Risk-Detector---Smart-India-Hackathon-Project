"""
Configuration settings for the Data Breach Risk Detector
Contains all constants, thresholds, and configuration values
"""

# Risk Score Thresholds
RISK_THRESHOLDS = {
    "LOW": 0,
    "MEDIUM": 30,
    "HIGH": 60,
    "CRITICAL": 90
}

# Risk Score Weights (how much each detection adds to risk)
RISK_WEIGHTS = {
    "public_api_exposed": 40,
    "failed_login_attempts": 20,
    "suspicious_access_time": 30,
    "missing_authentication": 35,
    "weak_password": 25,
    "multiple_ips": 15
}

# Detection Thresholds
DETECTION_CONFIG = {
    "max_failed_logins": 3,  # Failed login attempts before flagging
    "suspicious_hours": [0, 1, 2, 3, 4, 5],  # Hours considered suspicious (midnight to 5am)
    "rate_limit_threshold": 100  # API calls per minute threshold
}

# Database Configuration
DATABASE_PATH = "backend/database/breach_data.db"

# Server Configuration
SERVER_CONFIG = {
    "host": "127.0.0.1",
    "port": 8000,
    "debug": True
}

# Alert Severity Levels
ALERT_SEVERITY = {
    "INFO": "INFO",
    "WARNING": "WARNING",
    "CRITICAL": "CRITICAL"
}
