from typing import List, Dict


class KnowledgeBase:

    def __init__(self):
        self.documents = {
            "andean_climate": {
                "frost_peak_months": ["July", "August"],
                "frost_risk_threshold_celsius": -2,
                "typical_frost_occurrence": "Late July to mid-August",
                "crop_damage_risk": "Critical when frost occurs during flowering (3-6 weeks post-planting)",
                "source": "FAO Climate Data - Andean Region Historical Records",
            },
            "corn_subsistence": {
                "optimal_planting_window": "March to May",
                "growing_season_days": 120,
                "water_requirement_mm": 500,
                "critical_growth_stages": [
                    "Germination (0-10 days)",
                    "Vegetative (10-60 days)",
                    "Flowering (60-90 days)",
                    "Grain fill (90-120 days)",
                ],
                "flood_risk_threshold": 70,
                "drought_stress_threshold": 30,
                "source": "FAO Crop Water Information - Corn",
            },
            "irrigation_efficiency": {
                "drip_irrigation_efficiency": 0.95,
                "surface_irrigation_efficiency": 0.7,
                "investment_to_yield_ratio": 0.03,
                "water_stress_reduction_per_investment": 0.8,
                "source": "International Water Management Institute (IWMI)",
            },
            "soil_andean": {
                "clay_content": "High (>40%)",
                "drainage_classification": "Poor",
                "water_retention_capacity": "High",
                "compaction_risk": "High during wet season",
                "remediation": "Requires structured irrigation investment to prevent waterlogging",
                "source": "ISRIC Soil Database - Andean Region",
            },
        }

    def query(self, topic: str) -> Dict:
        return self.documents.get(topic, {"error": "Topic not found in knowledge base"})

    def search_related(self, keywords: List[str]) -> Dict[str, Dict]:
        results = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            for doc_key, doc_data in self.documents.items():
                if keyword_lower in doc_key:
                    results[doc_key] = doc_data
        return results

    def get_climate_risk_factors(self, region: str, planting_shift: float) -> Dict:
        if "andean" in region.lower():
            frost_risk = 95 - planting_shift * 10
            return {
                "region": region,
                "frost_risk_percentage": max(10, frost_risk),
                "critical_months": self.documents["andean_climate"][
                    "frost_peak_months"
                ],
                "frost_damage_threshold": self.documents["andean_climate"][
                    "frost_risk_threshold_celsius"
                ],
            }
        return {"region": region, "frost_risk_percentage": 50}

    def get_irrigation_impact(self, irrigation_level: float) -> Dict:
        efficiency = self.documents["irrigation_efficiency"]
        return {
            "investment_level": irrigation_level,
            "yield_increase_factor": efficiency["investment_to_yield_ratio"],
            "water_stress_reduction": efficiency[
                "water_stress_reduction_per_investment"
            ]
            * (irrigation_level / 100),
            "expected_soil_stabilization": (
                "Moderate to High" if irrigation_level > 50 else "Low"
            ),
        }
