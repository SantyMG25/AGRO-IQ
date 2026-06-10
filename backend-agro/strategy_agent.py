import asyncio
from typing import Dict, Any
from agents import Agent, AgentContext, AgentReport
from llm_config import call_llm


class StrategyAgent(Agent):

    def __init__(self):
        super().__init__(
            name="Strategy Agent", role="Predictive Analyst & Executive Advisor"
        )

    async def analyze(
        self, context: AgentContext, auditor_report: AgentReport
    ) -> AgentReport:
        auditor_findings = auditor_report.findings
        reasoning_steps = self._chain_of_thought_analysis(context, auditor_findings)
        findings = {
            "scenario_viability": reasoning_steps["scenario_assessment"],
            "risk_correlations": reasoning_steps["risk_correlations"],
            "investment_recommendation": reasoning_steps["investment_recommendation"],
            "critical_decision_points": reasoning_steps["critical_decisions"],
            "economic_projections": reasoning_steps["economic_impact"],
            "resilience_score": reasoning_steps["resilience_score"],
        }
        raw_analysis = await self._generate_executive_prediction_llm(
            context, reasoning_steps, auditor_findings
        )
        return AgentReport(
            agent_name=self.name,
            role=self.role,
            findings=findings,
            confidence=0.88,
            raw_analysis=raw_analysis,
        )

    def _chain_of_thought_analysis(
        self, context: AgentContext, auditor_findings: Dict
    ) -> Dict[str, Any]:
        irrigation = context.irrigation_investment
        shift = context.planting_window_shift
        frost_risk = auditor_findings["risk_assessment"]["frost_risk_score"]
        water_stress = auditor_findings["risk_assessment"]["water_stress_risk"]
        thermal_risk = auditor_findings["risk_assessment"]["thermal_coupling_risk"]
        if irrigation < 30 and abs(shift) > 2:
            scenario_viability = (
                "CRITICAL - Insufficient water security with significant timing risk"
            )
            resilience = 35
        elif irrigation > 60 and abs(shift) <= 1:
            scenario_viability = (
                "OPTIMAL - Strong infrastructure with minimal timing volatility"
            )
            resilience = 88
        elif irrigation >= 50 and abs(shift) <= 2:
            scenario_viability = (
                "VIABLE - Adequate infrastructure with manageable timing adjustments"
            )
            resilience = 72
        else:
            scenario_viability = "MODERATE - Balanced risk profile requiring monitoring"
            resilience = 58
        risk_correlations = {
            "irrigation_frost_dependency": irrigation > 50,
            "shift_water_stress_coupling": shift > 0 and water_stress > 60,
            "thermal_timing_conflict": abs(shift) > 1 and frost_risk > 80,
            "soil_infrastructure_link": water_stress > 60 and irrigation < 50,
        }
        if resilience >= 75:
            recommendation = (
                "PROCEED - Scenario demonstrates strong economic resilience"
            )
            priority = "Monitor monthly"
        elif resilience >= 55:
            recommendation = (
                "CONDITIONAL - Proceed with contingency planning for water months"
            )
            priority = "Weekly monitoring required"
        else:
            recommendation = (
                "EVALUATE ALTERNATIVES - Current configuration presents excessive risk"
            )
            priority = "Daily monitoring + immediate intervention triggers"
        critical_decisions = []
        if frost_risk > 80:
            critical_decisions.append(
                f"FROST ALERT: Risk at {frost_risk:.0f}%. Activate frost protection by late June."
            )
        if water_stress > 70:
            critical_decisions.append(
                f"WATER DEFICIT: Stress at {water_stress:.0f}%. Secure supplemental irrigation by week 4."
            )
        if thermal_risk > 60:
            critical_decisions.append(
                f"THERMAL COUPLING: Shift-induced risk at {thermal_risk:.0f}%. Adjust phenology monitoring."
            )
        base_yield = 2.5
        irrigation_multiplier = 1 + irrigation / 100 * 0.4
        shift_penalty = 1 - abs(shift) / 10 * 0.15
        projected_yield = base_yield * irrigation_multiplier * shift_penalty
        economic_impact = {
            "projected_yield_tons": round(projected_yield, 2),
            "market_price_per_ton": 200,
            "gross_revenue": round(projected_yield * 200, 2),
            "infrastructure_cost": irrigation * 50,
            "net_economic_benefit": round(projected_yield * 200 - irrigation * 50, 2),
        }
        return {
            "scenario_assessment": scenario_viability,
            "risk_correlations": risk_correlations,
            "investment_recommendation": recommendation,
            "monitoring_priority": priority,
            "critical_decisions": critical_decisions,
            "economic_impact": economic_impact,
            "resilience_score": resilience,
        }

    async def _generate_executive_prediction_llm(
        self, context: AgentContext, reasoning: Dict, auditor_findings: Dict
    ) -> str:
        prompt = f"""\nYou are an expert agricultural strategy advisor with deep expertise in predictive analytics \nand climate-resilient farming systems. Generate an executive-level strategic prediction report \nbased on the following simulation scenario and analysis:\n\nSCENARIO PARAMETERS:\n- Region: {context.region}\n- Crop Type: {context.crop_type}\n- Irrigation Investment: {context.irrigation_investment}%\n- Planting Window Shift: {context.planting_window_shift:+.0f} weeks\n- Fertilizer Subsidy: {context.fertilizer_subsidy}%\n\nCHAIN-OF-THOUGHT ANALYSIS RESULTS:\n- Scenario Viability: {reasoning['scenario_assessment']}\n- Resilience Score: {reasoning['resilience_score']}/100\n- Investment Recommendation: {reasoning['investment_recommendation']}\n- Projected Yield: {reasoning['economic_impact']['projected_yield_tons']:.2f} tons\n- Net Economic Benefit: ${reasoning['economic_impact']['net_economic_benefit']:.0f}\n\nRISK CORRELATIONS:\n{', '.join((f"{k.replace('_', ' ')}: {('Yes' if v else 'No')}" for k, v in reasoning['risk_correlations'].items()))}\n\nCRITICAL DECISIONS:\n{(chr(10).join((f'- {d}' for d in reasoning['critical_decisions'])) if reasoning['critical_decisions'] else '- No critical decisions identified')}\n\nGenerate a compelling 200-250 word executive prediction that:\n1. Synthesizes the numerical analysis into a coherent narrative\n2. Explains the strategic implications of this scenario\n3. Identifies unique opportunities or risks not obvious from numbers alone\n4. Provides actionable forward-looking guidance\n5. Maintains a professional but accessible tone for enterprise stakeholders\n\nFormat as a polished executive summary with key insights."""
        system_prompt = "You are a senior agricultural economist and climate resilience strategist \nadvising enterprise farming operations on ESG and food security outcomes. Provide strategic insight \nthat balances quantitative rigor with qualitative understanding of farming realities."
        report = await call_llm(prompt, system_prompt, temperature=0.7)
        return report
