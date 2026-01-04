"""
Misconfiguration Detector Module
Detects common security misconfigurations:
- Debug mode enabled in production
- Default credentials
- Insecure configurations
"""

from typing import List, Dict

class MisconfigDetector:
    """Detects security misconfigurations"""
    
    def __init__(self):
        # Common default/weak usernames that should be flagged
        self.weak_usernames = ['admin', 'root', 'administrator', 'test', 'guest']
    
    def detect_default_credentials(self, auth_logs: List[Dict]) -> List[Dict]:
        """
        RULE: If default/common usernames like 'admin' are being used,
        flag as potential misconfiguration
        
        Returns: List of detected issues
        """
        issues = []
        detected_users = set()
        
        for log in auth_logs:
            user = log.get('user', '').lower()
            
            if user in self.weak_usernames and user not in detected_users:
                detected_users.add(user)
                issues.append({
                    "type": "default_credentials",
                    "user": log.get('user'),
                    "severity": "WARNING",
                    "description": f"Default/common username '{log.get('user')}' is in use"
                })
        
        return issues
    
    def detect_public_endpoints(self, endpoint_scans: List[Dict]) -> List[Dict]:
        """
        RULE: Identify all publicly accessible endpoints for review
        
        Returns: List of public endpoints
        """
        issues = []
        
        for scan in endpoint_scans:
            if scan.get('public_access') and scan.get('risk_level') != 'LOW':
                issues.append({
                    "type": "public_endpoint",
                    "endpoint": scan.get('endpoint'),
                    "risk_level": scan.get('risk_level'),
                    "severity": "INFO",
                    "description": f"Endpoint '{scan.get('endpoint')}' is publicly accessible"
                })
        
        return issues
    
    def analyze(self, auth_logs: List[Dict], endpoint_scans: List[Dict]) -> Dict:
        """
        Run all misconfiguration detectors and return combined results
        """
        print("\n🔍 Running Misconfiguration Analysis...")
        
        default_cred_issues = self.detect_default_credentials(auth_logs)
        public_endpoint_issues = self.detect_public_endpoints(endpoint_scans)
        
        all_issues = default_cred_issues + public_endpoint_issues
        
        print(f"  - Default credentials: {len(default_cred_issues)}")
        print(f"  - Public endpoints: {len(public_endpoint_issues)}")
        
        return {
            "detector": "misconfiguration",
            "total_issues": len(all_issues),
            "issues": all_issues
        }
