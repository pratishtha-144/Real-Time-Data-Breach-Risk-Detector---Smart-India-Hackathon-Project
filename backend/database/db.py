"""
Database helper functions for storing and retrieving breach detection data
Uses simple JSON file storage for hackathon simplicity
"""

import json
import os
from datetime import datetime
from typing import List, Dict

# Database file paths
ALERTS_DB = "backend/database/alerts.json"
SCANS_DB = "backend/database/scans.json"

def init_db():
    """Initialize database files if they don't exist"""
    for db_file in [ALERTS_DB, SCANS_DB]:
        if not os.path.exists(db_file):
            os.makedirs(os.path.dirname(db_file), exist_ok=True)
            with open(db_file, 'w') as f:
                json.dump([], f)

def save_alert(alert: Dict):
    """Save an alert to the database"""
    init_db()
    
    # Read existing alerts
    with open(ALERTS_DB, 'r') as f:
        alerts = json.load(f)
    
    # Add new alert
    alerts.append(alert)
    
    # Save back to file
    with open(ALERTS_DB, 'w') as f:
        json.dump(alerts, f, indent=2)

def get_all_alerts() -> List[Dict]:
    """Retrieve all alerts from database"""
    init_db()
    
    with open(ALERTS_DB, 'r') as f:
        return json.load(f)

def get_recent_alerts(limit: int = 10) -> List[Dict]:
    """Get most recent alerts"""
    alerts = get_all_alerts()
    return alerts[-limit:] if len(alerts) > limit else alerts

def save_scan_result(scan_data: Dict):
    """Save a scan result to the database"""
    init_db()
    
    # Add timestamp
    scan_data['timestamp'] = datetime.now().isoformat()
    
    # Read existing scans
    with open(SCANS_DB, 'r') as f:
        scans = json.load(f)
    
    # Add new scan
    scans.append(scan_data)
    
    # Save back to file
    with open(SCANS_DB, 'w') as f:
        json.dump(scans, f, indent=2)

def get_latest_scan() -> Dict:
    """Get the most recent scan result"""
    init_db()
    
    with open(SCANS_DB, 'r') as f:
        scans = json.load(f)
    
    return scans[-1] if scans else None

def clear_alerts():
    """Clear all alerts (for testing)"""
    with open(ALERTS_DB, 'w') as f:
        json.dump([], f)
