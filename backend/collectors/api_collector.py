"""
API Collector Module
Simulates scanning for exposed API endpoints
In a real system, this would scan actual network endpoints
"""

from typing import List, Dict

class APICollector:
    """Collects information about API endpoints and their security"""
    
    def __init__(self):
        # Simulated list of API endpoints to check
        self.endpoints_to_scan = [
            "/api/users",
            "/api/admin/settings",
            "/api/database/dump",
            "/api/health",
            "/api/data/export"
        ]
    
    def scan_endpoints(self) -> List[Dict]:
        """
        Simulate scanning API endpoints for security issues
        In real implementation, this would make HTTP requests
        
        Returns: List of endpoint scan results
        """
        scan_results = []
        
        # Simulate scanning each endpoint
        for endpoint in self.endpoints_to_scan:
            result = self._simulate_endpoint_check(endpoint)
            scan_results.append(result)
        
        print(f"✓ Scanned {len(scan_results)} API endpoints")
        return scan_results
    
    def _simulate_endpoint_check(self, endpoint: str) -> Dict:
        """
        Simulate checking an endpoint for security issues
        This is simplified for hackathon demo purposes
        """
        # Simulate different security statuses based on endpoint name
        if "admin" in endpoint or "database" in endpoint or "dump" in endpoint:
            # These should be protected but we'll simulate they're exposed
            return {
                "endpoint": endpoint,
                "requires_auth": True,
                "auth_enforced": False,  # Vulnerability!
                "public_access": True,
                "risk_level": "HIGH"
            }
        elif "health" in endpoint:
            # Health endpoints are typically public
            return {
                "endpoint": endpoint,
                "requires_auth": False,
                "auth_enforced": False,
                "public_access": True,
                "risk_level": "LOW"
            }
        else:
            # Regular endpoints with proper auth
            return {
                "endpoint": endpoint,
                "requires_auth": True,
                "auth_enforced": True,
                "public_access": False,
                "risk_level": "LOW"
            }
    
    def get_exposed_endpoints(self, scan_results: List[Dict]) -> List[Dict]:
        """
        Filter scan results to find endpoints that should be protected but aren't
        """
        exposed = [
            result for result in scan_results
            if result.get('requires_auth') and not result.get('auth_enforced')
        ]
        return exposed
