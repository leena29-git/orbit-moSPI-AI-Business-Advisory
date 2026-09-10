from typing import Dict, Any


class SchemeMatcher:
    TRADITIONAL_CRAFTS = {
        "pottery", "carpentry", "blacksmith", "tailoring", 
        "weaving", "masonry", "goldsmith", "sculptor", "cobbler"
    }

    @classmethod
    def match_scheme(cls, profile: Dict[str, Any]) -> Dict[str, Any]:
        capital = float(profile.get("capital_available", 0))
        estimated_project_cost = float(profile.get("expenses", 0)) * 6 + capital
        trade_skill = profile.get("trade_skill", "").lower().strip()
        business_type = profile.get("business_type", "").lower().strip()

        if trade_skill in cls.TRADITIONAL_CRAFTS or business_type in cls.TRADITIONAL_CRAFTS:
            return {
                "matched_scheme": "PM-Vishwakarma",
                "scheme_type": "Artisan & Craftsperson Support",
                "max_collateral_free_loan": 300000,
                "subsidy_eligible": True,
                "reason": "Profile matches recognized traditional trades eligible for collateral-free credit and skill incentive under PM-Vishwakarma."
            }

        if estimated_project_cost > 100000:
            return {
                "matched_scheme": "PMEGP (Prime Minister's Employment Generation Programme)",
                "scheme_type": "Credit-Linked Subsidy (15-35%)",
                "max_collateral_free_loan": 2500000,
                "subsidy_eligible": True,
                "reason": "Project scale and capital expenditure qualify for PMEGP margin money subsidy support."
            }

        return {
            "matched_scheme": "PM-Mudra Yojana (Shishu Category)",
            "scheme_type": "Micro-credit up to ₹50,000",
            "max_collateral_free_loan": 50000,
            "subsidy_eligible": False,
            "reason": "Micro enterprise working capital requirements qualify directly for hassle-free Mudra Shishu financing."
        }