"""
Log Collector Module
Reads and processes sample log files (auth logs, API logs)
In a real system, this would connect to actual log sources
"""

import json
from typing import List, Dict

class LogCollector:
    """Collects and processes log data from various sources"""
    
    def __init__(self):
        self.auth_logs_path = "sample_logs/auth_logs.json"
        self.api_logs_path = "sample_logs/api_logs.json"
    
    def collect_auth_logs(self) -> List[Dict]:
        """
        Read authentication logs from file
        Returns: List of authentication events
        """
        try:
            with open(self.auth_logs_path, 'r') as f:
                logs = json.load(f)
            print(f"✓ Collected {len(logs)} authentication logs")
            return logs
        except FileNotFoundError:
            print(f"⚠ Warning: {self.auth_logs_path} not found")
            return []
        except json.JSONDecodeError:
            print(f"⚠ Warning: Invalid JSON in {self.auth_logs_path}")
            return []
    
    def collect_api_logs(self) -> List[Dict]:
        """
        Read API access logs from file
        Returns: List of API request events
        """
        try:
            with open(self.api_logs_path, 'r') as f:
                logs = json.load(f)
            print(f"✓ Collected {len(logs)} API logs")
            return logs
        except FileNotFoundError:
            print(f"⚠ Warning: {self.api_logs_path} not found")
            return []
        except json.JSONDecodeError:
            print(f"⚠ Warning: Invalid JSON in {self.api_logs_path}")
            return []
    
    def get_failed_login_attempts(self, auth_logs: List[Dict]) -> List[Dict]:
        """
        Filter logs to get only failed login attempts
        """
        failed_logins = [
            log for log in auth_logs 
            if log.get('action') == 'login_failed'
        ]
        return failed_logins
    
    def get_successful_logins(self, auth_logs: List[Dict]) -> List[Dict]:
        """
        Filter logs to get only successful logins
        """
        successful_logins = [
            log for log in auth_logs 
            if log.get('action') == 'login_success'
        ]
        return successful_logins
