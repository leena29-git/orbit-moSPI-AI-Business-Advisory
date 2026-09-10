from module_2_intelligence.hldi_engine import HLDIEngine
from module_2_intelligence.dpr_generator import DPRGenerator


def test_section_7_scenarios():
    print("================================================================")
    print("🎯 RUNNING SECTION 7 USE-CASE SCENARIOS (ORBIT ABSTRACT SPEC)")
    print("================================================================")

    engine = HLDIEngine()

    # Scenario 1: Rising CPI spending & Moderate density (Grocery)
    s1 = {
        "profile_id": "SCENARIO_01_GROCERY",
        "district_id": "DIST_01",
        "block_id": "BLK_101",
        "business_type": "grocery",
        "capital_available": 40000,
        "expenses": 6000,
        "trade_skill": "None"
    }
    r1 = engine.calculate_hldi(s1["profile_id"], s1["district_id"], s1["block_id"], s1["business_type"])
    print(f"\n[SCENARIO 1] Grocery in Growing Demand Block:")
    print(f" -> HLDI Score: {r1['hldi_score']}/100")
    print(f" -> Feasibility: {r1['contributing_factors']}")
    assert r1['hldi_score'] >= 65, "Scenario 1 should yield high demand score"

    # Scenario 2: Saturated market (Grocery in Beta Block) -> Suggest Alternative
    s2 = {
        "profile_id": "SCENARIO_02_SATURATED",
        "district_id": "DIST_01",
        "block_id": "BLK_102",
        "business_type": "grocery",
        "capital_available": 20000,
        "expenses": 4000,
        "trade_skill": "None"
    }
    r2 = engine.calculate_hldi(s2["profile_id"], s2["district_id"], s2["block_id"], s2["business_type"])
    print(f"\n[SCENARIO 2] Grocery in Saturated Block:")
    print(f" -> HLDI Score: {r2['hldi_score']}/100")
    print(f" -> Alternative Suggestion: {r2['suggested_alternative']}")
    assert r2['hldi_score'] < 45, "Scenario 2 should reflect market saturation"
    assert r2['suggested_alternative'] is not None, "Scenario 2 must suggest alternative category"

    # Scenario 3: Traditional Artisan Skill -> PM-Vishwakarma Matching
    s3 = {
        "profile_id": "SCENARIO_03_ARTISAN",
        "district_id": "DIST_01",
        "block_id": "BLK_101",
        "business_type": "carpentry",
        "capital_available": 15000,
        "expenses": 2500,
        "trade_skill": "carpentry"
    }
    r3 = engine.calculate_hldi(s3["profile_id"], s3["district_id"], s3["block_id"], s3["business_type"])
    dpr3 = DPRGenerator.generate_dpr_data(s3, r3)
    print(f"\n[SCENARIO 3] Traditional Artisan Profile:")
    print(f" -> Matched Scheme: {dpr3['matched_scheme']}")
    assert dpr3['matched_scheme'] == "PM-Vishwakarma", "Artisan must match PM-Vishwakarma"

    # Scenario 4: Higher Capital Enterprise -> PMEGP Matching
    s4 = {
        "profile_id": "SCENARIO_04_PMEGP",
        "district_id": "DIST_01",
        "block_id": "BLK_101",
        "business_type": "electronics_repair",
        "capital_available": 50000,
        "expenses": 15000,
        "trade_skill": "Technical"
    }
    r4 = engine.calculate_hldi(s4["profile_id"], s4["district_id"], s4["block_id"], s4["business_type"])
    dpr4 = DPRGenerator.generate_dpr_data(s4, r4)
    print(f"\n[SCENARIO 4] Capital-Intensive Enterprise:")
    print(f" -> Matched Scheme: {dpr4['matched_scheme']}")
    assert "PMEGP" in dpr4['matched_scheme'], "Scale should qualify for PMEGP"

    print("\n✅ ALL SECTION 7 SCENARIOS VERIFIED AND ACCURATE!")


if __name__ == "__main__":
    test_section_7_scenarios()