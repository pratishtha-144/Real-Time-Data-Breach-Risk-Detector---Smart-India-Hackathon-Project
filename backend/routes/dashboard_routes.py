"""
Dashboard API Routes
Provides REST API endpoints for the frontend dashboard
"""

from fastapi import APIRouter
from typing import Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from collectors.log_collector import LogCollector
from collectors.api_collector import APICollector
from detectors.auth_detector import AuthDetector
from detectors.api_detector import APIDetector
from detectors.misconfig_detector import MisconfigDetector
from risk_engine.risk_score import RiskScorer
from alerts.alert_manager import AlertManager
from database.db import save_scan_result, get_latest_scan, get_all_alerts

router = APIRouter()

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Data Breach Risk Detector API",
        "version": "1.0.0",
        "status": "running"
    }

@router.post("/scan")
async def run_scan() -> Dict:
    """
    Run a complete security scan
    
    This endpoint:
    1. Collects logs and API data
    2. Runs all detectors
    3. Calculates risk score
    4. Generates alerts
    
    Returns:
        Complete scan results with risk score and detected issues
    """
    print("\n" + "="*60)
    print("🚀 STARTING SECURITY SCAN")
    print("="*60)
    
    # Step 1: Collect data
    print("\n📥 Step 1: Collecting Data...")
    log_collector = LogCollector()
    api_collector = APICollector()
    
    auth_logs = log_collector.collect_auth_logs()
    api_logs = log_collector.collect_api_logs()
    endpoint_scans = api_collector.scan_endpoints()
    
    # Step 2: Run detectors
    print("\n🔍 Step 2: Running Security Detectors...")
    auth_detector = AuthDetector()
    api_detector = APIDetector()
    misconfig_detector = MisconfigDetector()
    
    auth_results = auth_detector.analyze(auth_logs)
    api_results = api_detector.analyze(api_logs, endpoint_scans)
    misconfig_results = misconfig_detector.analyze(auth_logs, endpoint_scans)
    
    # Combine all issues
    all_issues = (
        auth_results['issues'] + 
        api_results['issues'] + 
        misconfig_results['issues']
    )
    
    # Step 3: Calculate risk score
    print("\n📊 Step 3: Calculating Risk Score...")
    risk_scorer = RiskScorer()
    risk_data = risk_scorer.calculate_score(all_issues)
    recommendations = risk_scorer.get_recommendations(risk_data)
    
    # Step 4: Generate alerts
    print("\n🚨 Step 4: Generating Alerts...")
    alert_manager = AlertManager()
    alerts = alert_manager.process_issues(all_issues)
    alert_summary = alert_manager.get_alert_summary(alerts)
    
    # Prepare results
    scan_results = {
        "scan_completed": True,
        "risk_score": risk_data['score'],
        "risk_level": risk_data['risk_level'],
        "total_issues": len(all_issues),
        "issues_by_detector": {
            "authentication": auth_results['total_issues'],
            "api_security": api_results['total_issues'],
            "misconfiguration": misconfig_results['total_issues']
        },
        "all_issues": all_issues,
        "alert_summary": alert_summary,
        "recommendations": recommendations,
        "risk_breakdown": risk_data['breakdown']
    }
    
    # Save scan to database
    save_scan_result(scan_results)
    
    print("\n" + "="*60)
    print("✅ SCAN COMPLETED")
    print(f"   Risk Level: {risk_data['risk_level']}")
    print(f"   Total Issues: {len(all_issues)}")
    print("="*60)
    
    return scan_results

@router.get("/risk")
async def get_risk_score() -> Dict:
    """
    Get the latest risk score and summary
    
    Returns:
        Current risk level and score
    """
    latest_scan = get_latest_scan()
    
    if not latest_scan:
        return {
            "risk_score": 0,
            "risk_level": "UNKNOWN",
            "message": "No scans performed yet. Run /scan first."
        }
    
    return {
        "risk_score": latest_scan.get('risk_score'),
        "risk_level": latest_scan.get('risk_level'),
        "total_issues": latest_scan.get('total_issues'),
        "last_scan": latest_scan.get('timestamp')
    }

@router.get("/alerts")
async def get_alerts() -> Dict:
    """
    Get all security alerts
    
    Returns:
        List of all alerts with severity levels
    """
    all_alerts = get_all_alerts()
    
    # Generate summary
    summary = {
        'CRITICAL': 0,
        'WARNING': 0,
        'INFO': 0,
        'total': len(all_alerts)
    }
    
    for alert in all_alerts:
        severity = alert.get('severity', 'INFO')
        if severity in summary:
            summary[severity] += 1
    
    return {
        "total_alerts": len(all_alerts),
        "summary": summary,
        "alerts": all_alerts
    }

@router.get("/status")
async def get_system_status() -> Dict:
    """
    Get system status and health check
    
    Returns:
        System status information
    """
    latest_scan = get_latest_scan()
    
    return {
        "system": "operational",
        "last_scan": latest_scan.get('timestamp') if latest_scan else None,
        "detectors": ["auth", "api", "misconfig"],
        "collectors": ["logs", "api_scanner"]
    }
