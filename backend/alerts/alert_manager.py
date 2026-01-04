"""
Alert Manager
Manages security alerts and notifications
- Generates alerts from detected issues
- Sends notifications
- Logs alerts to database
"""

from datetime import datetime
from typing import List, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db import save_alert

class AlertManager:
    """Manages security alerts and notifications"""
    
    def __init__(self):
        self.alert_history = []
    
    def create_alert(self, issue: Dict) -> Dict:
        """
        Create an alert from a detected issue
        
        Args:
            issue: Dictionary containing issue details
        
        Returns:
            Alert dictionary
        """
        alert = {
            "id": len(self.alert_history) + 1,
            "timestamp": datetime.now().isoformat(),
            "severity": issue.get('severity', 'INFO'),
            "type": issue.get('type'),
            "description": issue.get('description'),
            "details": issue
        }
        
        return alert
    
    def process_issues(self, all_issues: List[Dict]) -> List[Dict]:
        """
        Process all detected issues and create alerts
        
        Args:
            all_issues: List of detected security issues
        
        Returns:
            List of created alerts
        """
        alerts = []
        
        for issue in all_issues:
            alert = self.create_alert(issue)
            alerts.append(alert)
            
            # Save to database
            save_alert(alert)
            
            # Print to console (for demo purposes)
            self._print_alert(alert)
        
        self.alert_history.extend(alerts)
        return alerts
    
    def _print_alert(self, alert: Dict):
        """Print alert to console with colored output"""
        severity = alert.get('severity')
        description = alert.get('description')
        timestamp = alert.get('timestamp')
        
        # Color codes for terminal
        severity_colors = {
            'CRITICAL': '🔴',
            'WARNING': '🟡',
            'INFO': '🔵'
        }
        
        icon = severity_colors.get(severity, '⚪')
        
        print(f"\n{icon} ALERT [{severity}]")
        print(f"   Time: {timestamp}")
        print(f"   {description}")
    
    def get_alert_summary(self, alerts: List[Dict]) -> Dict:
        """
        Generate summary of alerts by severity
        
        Returns:
            Dictionary with counts by severity level
        """
        summary = {
            'CRITICAL': 0,
            'WARNING': 0,
            'INFO': 0,
            'total': len(alerts)
        }
        
        for alert in alerts:
            severity = alert.get('severity', 'INFO')
            if severity in summary:
                summary[severity] += 1
        
        return summary
    
    def send_notification(self, alert: Dict):
        """
        Send notification for critical alerts
        In real implementation, this would send email/SMS/webhook
        For demo, we just log it
        """
        if alert.get('severity') == 'CRITICAL':
            print(f"📧 [SIMULATED] Email notification sent for critical alert: {alert.get('description')}")
