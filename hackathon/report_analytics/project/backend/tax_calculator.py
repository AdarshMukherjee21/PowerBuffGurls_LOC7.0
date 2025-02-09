from datetime import datetime
from typing import Dict, Any

def calculate_tax_benefits(contribution_amount: float) -> Dict[str, float]:
    """
    Calculate tax benefits based on CSR contributions using Section 80G rules.
    
    Args:
        contribution_amount: Total CSR contribution amount
        
    Returns:
        Dictionary containing deduction and tax saving details
    """
    # Section 80G allows 50% deduction for qualifying donations
    eligible_deduction = contribution_amount * 0.5
    
    # Assuming corporate tax rate of 30%
    tax_rate = 0.30
    estimated_tax_savings = eligible_deduction * tax_rate
    
    return {
        "eligible_deduction": eligible_deduction,
        "estimated_tax_savings": estimated_tax_savings
    }

def validate_csr_contribution(campaign_data: Dict[str, Any]) -> bool:
    """
    Validate if a CSR contribution qualifies for tax benefits.
    
    Args:
        campaign_data: Campaign details including cause, amount etc.
        
    Returns:
        Boolean indicating if contribution qualifies
    """
    qualifying_causes = [
        "Education",
        "Healthcare",
        "Environment",
        "Poverty",
        "Rural Development"
    ]
    
    # Basic validation rules
    if campaign_data.get("cause") not in qualifying_causes:
        return False
        
    if campaign_data.get("amount_raised", 0) <= 0:
        return False
        
    return True