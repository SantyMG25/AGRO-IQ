import asyncio
from typing import Dict
from agents import Agent, AgentContext, AgentReport
from microsoft_iq import microsoft_iq_connector
from llm_config import call_llm


class AuditorAgent(Agent):

    def __init__(self):
        super().__init__(
            name="Auditor Agent", role="Technical Validator & Knowledge Consultant"
        )

    async def analyze(self, context: AgentContext) -> AgentReport:
        climate_doc = await microsoft_iq_connector.query_foundry_iq(
            context.region, "climate"
        )
        irrigation_doc = await microsoft_iq_connector.query_foundry_iq(
            context.region, "irrigation"
        )
        soil_doc = await microsoft_iq_connector.query_foundry_iq(context.region, "soil")
        crop_doc = await microsoft_iq_connector.query_foundry_iq(context.region, "corn")
        fabric_telemetry = await microsoft_iq_connector.get_fabric_telemetry(
            context.region
        )
        climate_meta = climate_doc["retrieved_metadata"]
        frost_risk = 95 - context.planting_window_shift * 10
        climate_risks = {
            "region": context.region,
            "frost_risk_percentage": max(10, frost_risk),
            "critical_months": climate_meta["frost_peak_months"],
            "frost_damage_threshold": climate_meta["frost_risk_threshold_celsius"],
        }
        irrigation_meta = irrigation_doc["retrieved_metadata"]
        irrigation_impact = {
            "investment_level": context.irrigation_investment,
            "yield_increase_factor": irrigation_meta["investment_to_yield_ratio"],
            "water_stress_reduction": irrigation_meta[
                "water_stress_reduction_per_investment"
            ]
            * (context.irrigation_investment / 100),
            "expected_soil_stabilization": (
                "Moderate to High" if context.irrigation_investment > 50 else "Low"
            ),
        }
        soil_data = soil_doc["retrieved_metadata"]
        crop_data = crop_doc["retrieved_metadata"]
        findings = {
            "climate_analysis": climate_risks,
            "irrigation_analysis": irrigation_impact,
            "soil_conditions": {
                "type": soil_data["clay_content"],
                "drainage": soil_data["drainage_classification"],
                "water_retention": soil_data["water_retention_capacity"],
                "remediation_required": context.irrigation_investment < 50,
            },
            "crop_profile": {
                "type": context.crop_type,
                "water_requirement_mm": crop_data["water_requirement_mm"],
                "growing_season_days": crop_data["growing_season_days"],
                "critical_stages": crop_data["critical_growth_stages"],
            },
            "risk_assessment": {
                "frost_risk_score": climate_risks["frost_risk_percentage"],
                "water_stress_risk": max(0, 100 - context.irrigation_investment * 0.8),
                "thermal_coupling_risk": abs(context.planting_window_shift) * 15,
            },
            "microsoft_iq_metadata": {
                "foundry_iq": {
                    "status": "active",
                    "retrieved_documents": [
                        climate_doc["document_name"],
                        irrigation_doc["document_name"],
                        soil_doc["document_name"],
                        crop_doc["document_name"],
                    ],
                    "confidence": (
                        climate_doc["confidence_score"]
                        + irrigation_doc["confidence_score"]
                        + soil_doc["confidence_score"]
                        + crop_doc["confidence_score"]
                    )
                    / 4,
                },
                "fabric_iq": {
                    "status": "active",
                    "lakehouse": fabric_telemetry["lakehouse"],
                    "table_source": fabric_telemetry["table_source"],
                    "records_processed": fabric_telemetry["records_processed"],
                    "last_sync": fabric_telemetry["last_sync"],
                },
            },
        }
        raw_analysis = await self._generate_technical_report_llm(context, findings)
        return AgentReport(
            agent_name=self.name,
            role=self.role,
            findings=findings,
            confidence=0.92,
            raw_analysis=raw_analysis,
        )

    async def _generate_technical_report_llm(
        self, context: AgentContext, findings: Dict
    ) -> str:
        prompt = f"\nYou are an expert agricultural auditor analyzing a crop simulation scenario. \nProvide a technical audit report based on the following data:\n\nSCENARIO:\n- Region: {context.region}\n- Crop Type: {context.crop_type}\n- Irrigation Investment: {context.irrigation_investment}%\n- Planting Window Shift: {context.planting_window_shift} weeks\n- Fertilizer Subsidy: {context.fertilizer_subsidy}%\n\nKNOWLEDGE BASE FINDINGS:\n- Frost Risk: {findings['risk_assessment']['frost_risk_score']}%\n- Water Stress Risk: {findings['risk_assessment']['water_stress_risk']:.0f}%\n- Thermal Coupling Risk: {findings['risk_assessment']['thermal_coupling_risk']:.0f}%\n- Soil Type: {findings['soil_conditions']['type']}\n- Irrigation Impact: {findings['irrigation_analysis']['water_stress_reduction']:.1%} stress reduction\n- Expected Yield Increase: +{findings['irrigation_analysis']['yield_increase_factor'] * context.irrigation_investment:.1%}\n\nGenerate a concise technical audit report (150-200 words) that:\n1. Validates the scenario against FAO climate data\n2. Assesses technical feasibility\n3. Identifies key risks and opportunities\n4. Provides specific technical recommendations\n\nFormat as a professional technical assessment."
        system_prompt = "You are an expert agricultural consultant with deep knowledge of \nAndean farming systems, climate resilience, and crop optimization. Provide factual, evidence-based \nanalysis grounded in agronomic science."
        report = await call_llm(prompt, system_prompt, temperature=0.6)
        return report
