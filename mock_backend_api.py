"""
MOCK API ENDPOINTS FOR MODULE 1 (BACKEND TEAM) INTEGRATION
Provides clean JSON endpoints for Mobile App and Officer Dashboard.
"""
from module_2_intelligence import HLDIEngine, DPRGenerator

engine = HLDIEngine()


def api_get_hldi_score(profile_payload: dict) -> dict:
    """Invoked by Mobile App & Backend for HLDI score calculation."""
    return engine.calculate_hldi(
        profile_id=profile_payload["profile_id"],
        district_id=profile_payload["district_id"],
        block_id=profile_payload["block_id"],
        business_type=profile_payload["business_type"]
    )


def api_generate_dpr(profile_payload: dict) -> dict:
    """Invoked when citizen submits conversation data for DPR generation."""
    hldi_res = api_get_hldi_score(profile_payload)
    return DPRGenerator.generate_dpr_data(profile_payload, hldi_res)


def api_export_dpr_pdf(dpr_payload: dict, output_file_path: str) -> str:
    """Invoked by Officer Dashboard for downloading approved DPR PDF."""
    return DPRGenerator.export_dpr_pdf(dpr_payload, output_file_path)


if __name__ == "__main__":
    sample_request = {
        "profile_id": "ENT_DEMO_01",
        "district_id": "DIST_01",
        "block_id": "BLK_101",
        "business_type": "grocery",
        "capital_available": 30000,
        "expenses": 5000,
        "trade_skill": "None"
    }
    
    print("\n--- MOCK API: HLDI Score ---")
    print(api_get_hldi_score(sample_request))
    
    print("\n--- MOCK API: Auto-Generated DPR ---")
    print(api_generate_dpr(sample_request))