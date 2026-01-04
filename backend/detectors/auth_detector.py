"""
Authentication Detector Module
Detects suspicious authentication patterns that could indicate breach attempts:
- Multiple failed login attempts (brute force)
- Access at unusual times
- Multiple IPs for same user
"""

from typing import List, Dict
from datetime import datetime
from collections import defaultdict
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import DETECTION_CONFIG

class AuthDetector:
    """Detects authentication-related security issues"""
    
    def __init__(self):
        self.max_failed_logins = DETECTION_CONFIG['max_failed_logins']
        self.suspicious_hours = DETECTION_CONFIG['suspicious_hours']
    
    def detect_brute_force(self, auth_logs: List[Dict]) -> List[Dict]:
        """
        RULE: If a user has more than MAX_FAILED_LOGINS failed attempts,
        flag it as potential brute force attack
        
        Returns: List of detected issues
        """
        issues = []
        
        # Count failed logins per user
        failed_attempts = defaultdict(list)
        
        for log in auth_logs:
            if log.get('action') == 'login_failed':
                user = log.get('user')
                failed_attempts[user].append(log)
        
        # Check if any user exceeds threshold
        for user, attempts in failed_attempts.items():
            if len(attempts) > self.max_failed_logins:
                issues.append({
                    "type": "brute_force_detected",
                    "user": user,
                    "failed_attempts": len(attempts),
                    "ips": list(set([log.get('ip') for log in attempts])),
                    "severity": "CRITICAL",
                    "description": f"User '{user}' had {len(attempts)} failed login attempts"
                })
        
        return issues
    
    def detect_suspicious_access_time(self, auth_logs: List[Dict]) -> List[Dict]:
        """
        RULE: If a successful login happens during suspicious hours (midnight-5am),
        flag it as potentially suspicious
        
        Returns: List of detected issues
        """
        issues = []
        
        for log in auth_logs:
            if log.get('action') == 'login_success':
                timestamp = log.get('timestamp')
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    hour = dt.hour
                    
                    if hour in self.suspicious_hours:
                        issues.append({
                            "type": "suspicious_access_time",
                            "user": log.get('user'),
                            "timestamp": timestamp,
                            "hour": hour,
                            "ip": log.get('ip'),
                            "severity": "WARNING",
                            "description": f"User '{log.get('user')}' logged in at suspicious hour {hour}:00"
                        })
                except Exception as e:
                    continue
        
        return issues
    
    def detect_multiple_ip_access(self, auth_logs: List[Dict]) -> List[Dict]:
        """
        RULE: If a user successfully logs in from multiple different IPs,
        it could indicate credential sharing or compromise
        
        Returns: List of detected issues
        """
        issues = []
        
        # Group successful logins by user
        user_ips = defaultdict(set)
        
        for log in auth_logs:
            if log.get('action') == 'login_success':
                user = log.get('user')
                ip = log.get('ip')
                user_ips[user].add(ip)
        
        # Check for users with multiple IPs
        for user, ips in user_ips.items():
            if len(ips) > 1:
                issues.append({
                    "type": "multiple_ip_access",
                    "user": user,
                    "ip_count": len(ips),
                    "ips": list(ips),
                    "severity": "WARNING",
                    "description": f"User '{user}' logged in from {len(ips)} different IPs"
                })
        
        return issues
    
    def analyze(self, auth_logs: List[Dict]) -> Dict:
        """
        Run all authentication detectors and return combined results
        """
        print("\n🔍 Running Authentication Analysis...")
        
        brute_force_issues = self.detect_brute_force(auth_logs)
        suspicious_time_issues = self.detect_suspicious_access_time(auth_logs)
        multiple_ip_issues = self.detect_multiple_ip_access(auth_logs)
        
        all_issues = brute_force_issues + suspicious_time_issues + multiple_ip_issues
        
        print(f"  - Brute force attempts: {len(brute_force_issues)}")
        print(f"  - Suspicious time access: {len(suspicious_time_issues)}")
        print(f"  - Multiple IP access: {len(multiple_ip_issues)}")
        
        return {
            "detector": "authentication",
            "total_issues": len(all_issues),
            "issues": all_issues
        }
