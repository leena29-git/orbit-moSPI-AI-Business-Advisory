import json
import os
from typing import Dict, Any, Tuple, Optional


class HLDIEngine:
    def __init__(self, data_file_path: Optional[str] = None):
        if data_file_path is None:
            base_dir = os.path.dirname(__file__)
            data_file_path = os.path.join(base_dir, "sample_mospi_data.json")
        
        with open(data_file_path, "r", encoding="utf-8") as f:
            self.mospi_data = json.load(f)

    def calculate_hldi(
        self, profile_id: str, district_id: str, block_id: str, business_type: str
    ) -> Dict[str, Any]:
        biz_key = business_type.lower().strip()
        dist = self.mospi_data.get("districts", {}).get(district_id)
        
        if not dist:
            return self._fallback_response(profile_id, "District not found in MoSPI cache.")
        
        block = dist.get("blocks", {}).get(block_id)
        if not block:
            return self._fallback_response(profile_id, "Block not found in MoSPI cache.")

        density_dict = block.get("enterprise_density", {})
        demand_dict = block.get("demand_growth_signals", {})
        
        density = density_dict.get(biz_key, 10)
        demand_growth = demand_dict.get(biz_key, 0.5)
        spending_idx = block.get("cpi_spending_index", 50.0)

        # Calibrated MoSPI HLDI Formulation:
        # High demand signal (up to 55 pts) + High CPI spending (up to 35 pts) - Saturation penalty (density)
        demand_score = demand_growth * 55.0
        spending_score = (spending_idx / 100.0) * 35.0
        density_penalty = min(density * 1.2, 25.0)

        raw_score = demand_score + spending_score - density_penalty + 10.0
        hldi_score = int(max(5, min(95, round(raw_score))))

        explanation, suggested_alt = self._generate_explanation_and_alt(
            biz_key, hldi_score, density, demand_growth, spending_idx, density_dict, demand_dict
        )

        return {
            "profile_id": profile_id,
            "hldi_score": hldi_score,
            "contributing_factors": explanation,
            "suggested_alternative": suggested_alt,
            "metrics_breakdown": {
                "enterprise_density": density,
                "cpi_spending_index": spending_idx,
                "demand_signal": demand_growth
            }
        }

    def _generate_explanation_and_alt(
        self, biz_key: str, score: int, density: int, demand: float, spending: float,
        all_densities: Dict[str, int], all_demands: Dict[str, float]
    ) -> Tuple[str, Optional[str]]:
        if score >= 65:
            exp = (f"High demand signal ({int(demand*100)}%) and strong local spending trend ({spending}/100) "
                   f"with manageable enterprise density ({density} existing units) in this block.")
            alt = None
        elif score >= 45:
            exp = (f"Moderate feasibility. Stable local spending, but existing competition ({density} units) "
                   f"requires cautious capital allocation.")
            alt = None
        else:
            exp = (f"Market saturation risk. High existing enterprise count ({density} units) "
                   f"relative to local spending growth.")
            candidates = []
            for k, dem in all_demands.items():
                if k != biz_key:
                    den = all_densities.get(k, 10)
                    potential = (dem * 50) - (den * 2)
                    candidates.append((k, potential))
            candidates.sort(key=lambda x: x[1], reverse=True)
            alt = candidates[0][0].replace("_", " ").title() if candidates else "Handicrafts / Artisanal Work"

        return exp, alt

    def _fallback_response(self, profile_id: str, reason: str) -> Dict[str, Any]:
        return {
            "profile_id": profile_id,
            "hldi_score": 50,
            "contributing_factors": f"Standard baseline score applied. {reason}",
            "suggested_alternative": None,
            "metrics_breakdown": {}
        }
