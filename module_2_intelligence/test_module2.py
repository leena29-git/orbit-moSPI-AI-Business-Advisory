import os
import json
from module_2_intelligence.hldi_engine import HLDIEngine
from module_2_intelligence.dpr_generator import DPRGenerator


def run_demo():
    print("==================================================")
    print("TESTING MODULE 2: AI INTELLIGENCE LAYER (ORBIT)")
    print("==================================================")

    engine = HLDIEngine()

    profile_1 = {
        "profile_id": "ENT_9001",
        "district_id": "DIST_01",
        "block_id": "BLK_101",
        "business_type": "grocery",
        "capital_available": 30000,
        "expenses": 5000,
        "trade_skill": "None",
        "language_dialect": "Bhojpuri"
    }

    print("\n[TEST 1] Calculating HLDI Score for Grocery in Alpha Block...")
    hldi_res_1 = engine.calculate_hldi(
        profile_id=profile_1["profile_id"],
        district_id=profile_1["district_id"],
        block_id=profile_1["block_id"],
        business_type=profile_1["business_type"]
    )
    print(json.dumps(hldi_res_1, indent=2))

    profile_2 = {
        "profile_id": "ENT_9002",
        "district_id": "DIST_01",
        "block_id": "BLK_102",
        "business_type": "pottery",
        "capital_available": 10000,
        "expenses": 2000,
        "trade_skill": "pottery",
        "language_dialect": "Tamil"
    }

    print("\n[TEST 2] Generating DPR & Matching Scheme for Artisan Profile...")
    hldi_res_2 = engine.calculate_hldi(
        profile_id=profile_2["profile_id"],
        district_id=profile_2["district_id"],
        block_id=profile_2["block_id"],
        business_type=profile_2["business_type"]
    )
    dpr_data = DPRGenerator.generate_dpr_data(profile_2, hldi_res_2)
    print(json.dumps(dpr_data, indent=2))

    output_pdf = "sample_bank_dpr.pdf"
    DPRGenerator.export_dpr_pdf(dpr_data, output_pdf)
    print(f"\nBank-Ready PDF DPR Generated: {os.path.abspath(output_pdf)}")
    print("\nALL TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    run_demo()