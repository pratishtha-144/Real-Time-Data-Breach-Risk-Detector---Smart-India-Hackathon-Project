"""
API Exposure Detector Module
Detects API security issues:
- Missing authentication tokens on sensitive endpoints
- Publicly accessible admin endpoints
"""

from typing import List, Dict

class APIDetector:
    """Detects API exposure and authentication issues"""
    
    def __init__(self):
        # Endpoints that should always require authentication
        self.protected_endpoints = [
            "/api/admin",
            "/api/database",
            "/api/users",
            "/api/data"
        ]
    
    def detect_missing_auth(self, api_logs: List[Dict]) -> List[Dict]:
        """
        RULE: If a sensitive endpoint is accessed without an auth token,
        flag it as a security issue
        
        Returns: List of detected issues
        """
        issues = []
        
        for log in api_logs:
            endpoint = log.get('endpoint', '')
            auth_token = log.get('auth_token')
            
            # Check if this is a protected endpoint
            is_protected = any(protected in endpoint for protected in self.protected_endpoints)
            
            if is_protected and not auth_token:
                issues.append({
                    "type": "missing_authentication",
                    "endpoint": endpoint,
                    "ip": log.get('ip'),
                    "timestamp": log.get('timestamp'),
                    "severity": "CRITICAL",
                    "description": f"Protected endpoint '{endpoint}' accessed without authentication"
                })
        
        return issues
    
    def detect_exposed_admin_endpoints(self, endpoint_scans: List[Dict]) -> List[Dict]:
        """
        RULE: If admin/database endpoints are publicly accessible,
        flag as critical vulnerability
        
        Returns: List of detected issues
        """
        issues = []
        
        for scan in endpoint_scans:
            endpoint = scan.get('endpoint', '')
            requires_auth = scan.get('requires_auth', False)
            auth_enforced = scan.get('auth_enforced', False)
            
            # Check if endpoint should be protected but isn't
            if requires_auth and not auth_enforced:
                severity = "CRITICAL" if ("admin" in endpoint or "database" in endpoint) else "WARNING"
                
                issues.append({
                    "type": "exposed_endpoint",
                    "endpoint": endpoint,
                    "public_access": scan.get('public_access'),
                    "severity": severity,
                    "description": f"Sensitive endpoint '{endpoint}' is publicly accessible"
                })
        
        return issues
    
    def analyze(self, api_logs: List[Dict], endpoint_scans: List[Dict]) -> Dict:
        """
        Run all API security detectors and return combined results
        """
        print("\n🔍 Running API Security Analysis...")
        
        missing_auth_issues = self.detect_missing_auth(api_logs)
        exposed_endpoint_issues = self.detect_exposed_admin_endpoints(endpoint_scans)
        
        all_issues = missing_auth_issues + exposed_endpoint_issues
        
        print(f"  - Missing authentication: {len(missing_auth_issues)}")
        print(f"  - Exposed endpoints: {len(exposed_endpoint_issues)}")
        
        return {
            "detector": "api_security",
            "total_issues": len(all_issues),
            "issues": all_issues
        }
