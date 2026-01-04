"""
Risk Scoring Engine
Calculates overall risk score based on detected issues
Each issue type contributes different points to total risk
"""

from typing import List, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import RISK_WEIGHTS, RISK_THRESHOLDS

class RiskScorer:
    """Calculates risk scores based on detected security issues"""
    
    def __init__(self):
        self.weights = RISK_WEIGHTS
        self.thresholds = RISK_THRESHOLDS
    
    def calculate_score(self, all_issues: List[Dict]) -> Dict:
        """
        Calculate total risk score based on all detected issues
        
        Scoring logic:
        - Each issue type has a weight (points added to risk)
        - Multiple instances of same issue type add up
        - Final score determines risk level: LOW/MEDIUM/HIGH/CRITICAL
        
        Returns: Dictionary with score, level, and breakdown
        """
        score = 0
        breakdown = {}
        
        # Count issues by type
        issue_counts = {}
        for issue in all_issues:
            issue_type = issue.get('type')
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        # Calculate score for each issue type
        for issue_type, count in issue_counts.items():
            weight = self._get_weight(issue_type)
            contribution = weight * count
            score += contribution
            
            breakdown[issue_type] = {
                "count": count,
                "weight": weight,
                "contribution": contribution
            }
        
        # Determine risk level
        risk_level = self._get_risk_level(score)
        
        print(f"\n📊 Risk Score Calculation:")
        print(f"  Total Score: {score}")
        print(f"  Risk Level: {risk_level}")
        
        return {
            "score": score,
            "risk_level": risk_level,
            "breakdown": breakdown,
            "total_issues": len(all_issues),
            "issue_counts": issue_counts
        }
    
    def _get_weight(self, issue_type: str) -> int:
        """Get the risk weight for an issue type"""
        # Map issue types to weights
        weight_mapping = {
            "exposed_endpoint": self.weights['public_api_exposed'],
            "missing_authentication": self.weights['missing_authentication'],
            "brute_force_detected": self.weights['failed_login_attempts'],
            "suspicious_access_time": self.weights['suspicious_access_time'],
            "default_credentials": self.weights['weak_password'],
            "multiple_ip_access": self.weights['multiple_ips'],
            "public_endpoint": 10  # Lower weight for info-level issues
        }
        
        return weight_mapping.get(issue_type, 5)  # Default weight if not mapped
    
    def _get_risk_level(self, score: int) -> str:
        """Determine risk level based on score"""
        if score >= self.thresholds['CRITICAL']:
            return "CRITICAL"
        elif score >= self.thresholds['HIGH']:
            return "HIGH"
        elif score >= self.thresholds['MEDIUM']:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_recommendations(self, risk_data: Dict) -> List[str]:
        """
        Provide security recommendations based on detected issues
        """
        recommendations = []
        
        issue_counts = risk_data.get('issue_counts', {})
        
        if 'brute_force_detected' in issue_counts:
            recommendations.append("🔒 Implement account lockout after failed login attempts")
            recommendations.append("🔒 Enable multi-factor authentication (MFA)")
        
        if 'exposed_endpoint' in issue_counts or 'missing_authentication' in issue_counts:
            recommendations.append("🔒 Add authentication to all sensitive API endpoints")
            recommendations.append("🔒 Implement API key validation")
        
        if 'suspicious_access_time' in issue_counts:
            recommendations.append("🔒 Set up alerts for off-hours access")
            recommendations.append("🔒 Review access logs regularly")
        
        if 'default_credentials' in issue_counts:
            recommendations.append("🔒 Change all default usernames and passwords")
            recommendations.append("🔒 Enforce strong password policies")
        
        if 'multiple_ip_access' in issue_counts:
            recommendations.append("🔒 Implement IP whitelisting for admin accounts")
            recommendations.append("🔒 Monitor for unusual login patterns")
        
        if not recommendations:
            recommendations.append("✓ No critical issues detected - maintain current security posture")
        
        return recommendations
