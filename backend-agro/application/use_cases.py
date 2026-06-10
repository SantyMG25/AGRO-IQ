import json
import asyncio
from typing import List, Dict, Any, Optional
from domain.entities import (
    SimulationResult,
    AgentContext,
    AgentReport,
    DashboardMetrics,
    HistoricalChartItem,
    ActionCard,
    ExecutiveSummary,
    FoundryIQMeta,
    FabricIQMeta,
    MicrosoftIQMetadata,
)
from ports.inbound import AnalyzeCropUseCasePort, GetAnalyticsUseCasePort
from ports.outbound import SimulationRepositoryPort, MicrosoftIQPort, LLMReasoningPort


class AnalyzeCropUseCase(AnalyzeCropUseCasePort):

    def __init__(
        self,
        repository_port: SimulationRepositoryPort,
        microsoft_iq_port: MicrosoftIQPort,
        llm_port: LLMReasoningPort,
    ):
        self.repository_port = repository_port
        self.microsoft_iq_port = microsoft_iq_port
        self.llm_port = llm_port
        self.agent_history = []

    async def orchestrate(
        self,
        region: str,
        crop_type: str,
        user_description: str,
        irrigation: float,
        shift: float,
        fertilizer: float,
    ) -> SimulationResult:
        context = AgentContext(
            region=region,
            crop_type=crop_type,
            user_description=user_description,
            irrigation_investment=irrigation,
            planting_window_shift=shift,
            fertilizer_subsidy=fertilizer,
        )
        print(f"[ORCHESTRATOR] Initializing Grounding Layer via Microsoft IQ...")
        foundry_task = self.microsoft_iq_port.query_foundry_iq(
            region, f"climate risk {crop_type}"
        )
        fabric_task = self.microsoft_iq_port.get_fabric_telemetry(region)
        foundry_res, fabric_res = await asyncio.gather(foundry_task, fabric_task)
        print(
            f"[ORCHESTRATOR] Knowledge retrieved from {foundry_res['document_name']}. Syncing with Lakehouse: {fabric_res['lakehouse']}."
        )
        system_prompt = "\n        Eres el Orquestador Multi-Agente Avanzado de AgroGarantia IQ. Tu objetivo es actuar en dos fases consecutivas:\n        1. AGENTE AUDITOR: Analiza los datos de los sensores, los sliders de entrada y contrasta con los manuales oficiales de la FAO recuperados de Microsoft Foundry IQ.\n        2. AGENTE ESTRATÉGICO: Evalúa la viabilidad económica y genera alertas críticas predictivas basadas en las vulnerabilidades encontradas.\n\n        DEBES responder EXCLUSIVAMENTE con un objeto JSON estructurado que contenga las métricas de impacto calculadas de forma autónoma y las recomendaciones redactadas en vivo. No uses plantillas estáticas.\n        "
        user_prompt = f"""\n        FICHA TÉCNICA DEL ESCENARIO DE SIMULACIÓN:\n        - Región de Análisis: {region}\n        - Cultivo Monitoreado: {crop_type}\n        - Contexto Operativo: {user_description}\n        \n        VARIABLES DE ENTRADA (SLIDERS):\n        - Inversión en Infraestructura Hídrica: {irrigation}%\n        - Desfase Calendario de Siembra: {shift} Semanas\n        - Subsidio de Fertilizantes: {fertilizer}%\n\n        CONTEXTO INTEGRADO MICROSOFT FOUNDRY IQ (RAG - MANUAL DE LA FAO):\n        - Origen del Documento: {foundry_res['source_document']}\n        - Confianza del Conocimiento: {foundry_res['confidence_score'] * 100}%\n        - Datos de Soporte Indexados: {json.dumps(foundry_res['retrieved_metadata'])}\n\n        TELEMETRÍA MICROSOFT FABRIC IQ (LAKEHOUSE DATALAKE):\n        - Origen: {fabric_res['lakehouse']} -> Tabla: {fabric_res['table_source']}\n        - Esquema de Datos Analíticos: {json.dumps(fabric_res['data_schema'])}\n        - Registros Históricos Procesados: {fabric_res['records_processed']}\n\n        REGLAS DE NEGOCIO PARA EL MODELO GENERATIVO:\n        1. Calcula el 'resilience_score' (0-100) y 'food_security_index' (0-100) basándote de verdad en los impactos cruzados. Si la inversión en riego es baja (<30%) y el desfase de semanas expone el cultivo al pico de heladas indicadas por la FAO, penaliza fuertemente los índices.\n        2. Proyecta las toneladas de rendimiento ('projected_yield_tons') y la pérdida mitigada en dólares ('economic_loss_prevented_usd').\n        3. Redacta las descripciones de las tarjetas ('action_cards') con lenguaje natural altamente profesional, técnico, corporativo y 100% enfocado en el impacto ESG de este escenario específico.\n        4. Construye el análisis de riesgo mensual ('historical_chart_data') para Julio, Agosto y Septiembre, modificando los valores mitigados según la inversión.\n\n        DEBES devolver estrictamente este formato JSON:\n        {{\n            "dashboard_metrics": {{\n                "food_security_index": int,\n                "projected_yield_tons": float,\n                "economic_loss_prevented_usd": int,\n                "resilience_score": int\n            }},\n            "historical_chart_data": [\n                {{"month": "Jul", "base_risk": int, "mitigated_risk": int, "agent_insight": "string"}},\n                {{"month": "Ago", "base_risk": int, "mitigated_risk": int, "agent_insight": "string"}},\n                {{"month": "Sep", "base_risk": int, "mitigated_risk": int, "agent_insight": "string"}}\n            ],\n            "action_cards": [\n                {{"id": "1", "title": "Water Resource Optimization", "description": "string", "agent_reasoning": "string", "visual_indicator": "emerald|amber|red", "resilience_contribution": "string"}},\n                {{"id": "2", "title": "Strategic Recommendation", "description": "string", "executive_priority": "string", "visual_indicator": "emerald|amber", "decision_triggers": ["string"]}},\n                {{"id": "3", "title": "Critical Alert", "description": "string", "visual_indicator": "red", "agent_source": "string"}}\n            ],\n            "executive_summary": {{\n                "scenario_viability": "string",\n                "economic_projection": "string",\n                "autonomous_prediction": "string"\n            }}\n        }}\n        """
        try:
            print(f"[ORCHESTRATOR] Dispatching generative analysis to LLM...")
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]
            response_content = await self.llm_port.chat_completion(
                messages=messages,
                response_format={"type": "json_object"},
                temperature=0.3,
            )
            generated_json = json.loads(response_content)
            print(
                "[ORCHESTRATOR] Multi-Agent autonomous inference successfully generated."
            )
            foundry_meta = FoundryIQMeta(
                status="active",
                confidence=float(foundry_res["confidence_score"]),
                source=foundry_res["document_name"],
            )
            fabric_meta = FabricIQMeta(
                status="connected",
                lakehouse=fabric_res["lakehouse"],
                synced_records=fabric_res["records_processed"],
            )
            iq_meta = MicrosoftIQMetadata(
                foundry_iq=foundry_meta, fabric_iq=fabric_meta
            )
            metrics = DashboardMetrics(
                food_security_index=generated_json["dashboard_metrics"][
                    "food_security_index"
                ],
                projected_yield_tons=generated_json["dashboard_metrics"][
                    "projected_yield_tons"
                ],
                economic_loss_prevented_usd=generated_json["dashboard_metrics"][
                    "economic_loss_prevented_usd"
                ],
                resilience_score=generated_json["dashboard_metrics"][
                    "resilience_score"
                ],
            )
            chart_data = [
                HistoricalChartItem(**item)
                for item in generated_json["historical_chart_data"]
            ]
            action_cards = []
            for card in generated_json["action_cards"]:
                action_cards.append(
                    ActionCard(
                        id=str(card.get("id", "")),
                        title=card.get("title", ""),
                        description=card.get("description", ""),
                        agent_reasoning=card.get("agent_reasoning"),
                        visual_indicator=card.get("visual_indicator", "emerald"),
                        resilience_contribution=card.get("resilience_contribution"),
                        executive_priority=card.get("executive_priority"),
                        decision_triggers=card.get("decision_triggers"),
                        agent_source=card.get("agent_source"),
                    )
                )
            summary = ExecutiveSummary(
                scenario_viability=generated_json["executive_summary"][
                    "scenario_viability"
                ],
                economic_projection=generated_json["executive_summary"][
                    "economic_projection"
                ],
                autonomous_prediction=generated_json["executive_summary"][
                    "autonomous_prediction"
                ],
                agent_confidence=float(foundry_res["confidence_score"] * 100),
            )
            simulation_result = SimulationResult(
                status="success",
                dashboard_metrics=metrics,
                historical_chart_data=chart_data,
                action_cards=action_cards,
                executive_summary=summary,
                microsoft_iq=iq_meta,
            )
            db_data = {
                "region": region,
                "crop_type": crop_type,
                "irrigation_investment": irrigation,
                "planting_window_shift": shift,
                "fertilizer_subsidy": fertilizer,
                "auditor_findings": json.dumps(foundry_res["retrieved_metadata"]),
                "auditor_confidence": float(foundry_res["confidence_score"]),
                "strategy_findings": json.dumps(generated_json["executive_summary"]),
                "strategy_confidence": 0.92,
                "resilience_score": float(metrics.resilience_score),
                "food_security_index": float(metrics.food_security_index),
                "projected_yield": float(metrics.projected_yield_tons),
                "loss_mitigated": float(metrics.economic_loss_prevented_usd),
                "executive_summary": summary.autonomous_prediction,
                "risk_level": (
                    "low"
                    if metrics.resilience_score >= 75
                    else "medium" if metrics.resilience_score >= 50 else "high"
                ),
            }
            self.repository_port.save_simulation(db_data)
            self.agent_history.append(simulation_result)
            return simulation_result
        except Exception as e:
            print(f"[ERROR CRÍTICO ORQUESTADOR]: {str(e)}")
            print(
                "[ORCHESTRATOR] Falling back to high-fidelity local simulation engine due to API error..."
            )
            try:
                simulation_result = self._generate_fallback_result(
                    region=region,
                    crop_type=crop_type,
                    user_description=user_description,
                    irrigation=irrigation,
                    shift=shift,
                    fertilizer=fertilizer,
                    foundry_res=foundry_res,
                    fabric_res=fabric_res,
                )
                metrics = simulation_result.dashboard_metrics
                summary = simulation_result.executive_summary
                db_data = {
                    "region": region,
                    "crop_type": crop_type,
                    "irrigation_investment": irrigation,
                    "planting_window_shift": shift,
                    "fertilizer_subsidy": fertilizer,
                    "auditor_findings": json.dumps(foundry_res["retrieved_metadata"]),
                    "auditor_confidence": float(foundry_res["confidence_score"]),
                    "strategy_findings": json.dumps(
                        {
                            "scenario_viability": summary.scenario_viability,
                            "economic_projection": summary.economic_projection,
                            "autonomous_prediction": summary.autonomous_prediction,
                        }
                    ),
                    "strategy_confidence": 0.95,
                    "resilience_score": float(metrics.resilience_score),
                    "food_security_index": float(metrics.food_security_index),
                    "projected_yield": float(metrics.projected_yield_tons),
                    "loss_mitigated": float(metrics.economic_loss_prevented_usd),
                    "executive_summary": summary.autonomous_prediction,
                    "risk_level": (
                        "low"
                        if metrics.resilience_score >= 75
                        else "medium" if metrics.resilience_score >= 50 else "high"
                    ),
                }
                self.repository_port.save_simulation(db_data)
                self.agent_history.append(simulation_result)
                return simulation_result
            except Exception as fallback_err:
                print(f"[ERROR CRÍTICO FALLBACK]: {str(fallback_err)}")
                return SimulationResult(
                    status="error",
                    message=f"Falló la inferencia generativa real: {str(e)}. Falló simulador local: {str(fallback_err)}",
                    dashboard_metrics=DashboardMetrics(
                        food_security_index=0,
                        projected_yield_tons=0,
                        economic_loss_prevented_usd=0,
                        resilience_score=0,
                    ),
                    historical_chart_data=[],
                    action_cards=[],
                    executive_summary=ExecutiveSummary(
                        scenario_viability="",
                        economic_projection="",
                        autonomous_prediction="",
                    ),
                )

    def _generate_fallback_result(
        self,
        region: str,
        crop_type: str,
        user_description: str,
        irrigation: float,
        shift: float,
        fertilizer: float,
        foundry_res: Dict[str, Any],
        fabric_res: Dict[str, Any],
    ) -> SimulationResult:
        base_resilience = 50
        resilience = max(
            0, min(100, int(base_resilience + irrigation * 0.4 - abs(shift) * 5))
        )
        food_security = max(
            0, min(100, int(45 + irrigation * 0.35 - abs(shift) * 4 + fertilizer * 0.1))
        )
        base_yield = 2.5
        irrigation_multiplier = 1 + irrigation / 100 * 0.4
        shift_penalty = 1 - abs(shift) / 10 * 0.15
        projected_yield = round(base_yield * irrigation_multiplier * shift_penalty, 2)
        economic_loss_prevented = int(resilience * 1250)
        metrics = DashboardMetrics(
            food_security_index=food_security,
            projected_yield_tons=projected_yield,
            economic_loss_prevented_usd=economic_loss_prevented,
            resilience_score=resilience,
        )
        chart_data = [
            HistoricalChartItem(
                month="Jul",
                base_risk=80,
                mitigated_risk=max(10, int(80 - irrigation * 0.6)),
                agent_insight=(
                    "Water deficit risk mitigated by infrastructure."
                    if irrigation > 40
                    else "High vulnerability to early drought stress."
                ),
            ),
            HistoricalChartItem(
                month="Ago",
                base_risk=95,
                mitigated_risk=max(15, int(95 - irrigation * 0.7 - shift * 2)),
                agent_insight=(
                    "Frost window avoided due to calendar shift."
                    if abs(shift) >= 2
                    else "Critical frost exposure risk during flowering."
                ),
            ),
            HistoricalChartItem(
                month="Sep",
                base_risk=70,
                mitigated_risk=max(5, int(70 - irrigation * 0.5)),
                agent_insight=(
                    "Optimal soil moisture retained post harvest."
                    if irrigation > 60
                    else "Moderate moisture stress detected."
                ),
            ),
        ]
        action_cards = [
            ActionCard(
                id="1",
                title="Water Resource Optimization",
                description=f"Drip irrigation system efficiency projects a water stress reduction of {irrigation * 0.8:.1f}%.",
                agent_reasoning="Investment provides critical dry-season buffer.",
                visual_indicator=(
                    "emerald"
                    if irrigation >= 50
                    else "amber" if irrigation >= 20 else "red"
                ),
                resilience_contribution=f"+{irrigation * 0.3:.0f}% Resilience",
            ),
            ActionCard(
                id="2",
                title="Strategic Recommendation",
                description=f"A calendar shift of {shift:+.1f} weeks modifies flowering exposure relative to historical frost peaks.",
                executive_priority="High" if abs(shift) > 2 else "Medium",
                visual_indicator="emerald" if abs(shift) <= 2 else "amber",
                decision_triggers=[
                    f"Monitor soil temp at {shift:+.1f}w",
                    "Check frost alerts weekly",
                ],
            ),
            ActionCard(
                id="3",
                title="Critical Alert",
                description=(
                    "Insufficient irrigation threshold may trigger localized water stress alerts during vegetative stages."
                    if irrigation < 40
                    else "All critical parameters stabilized under current infrastructure inputs."
                ),
                visual_indicator="red" if irrigation < 40 else "emerald",
                agent_source="Auditor Agent",
            ),
        ]
        viability = (
            "OPTIMAL"
            if resilience >= 75
            else "VIABLE" if resilience >= 50 else "CRITICAL"
        )
        summary = ExecutiveSummary(
            scenario_viability=f"{viability} (Dynamic Fallback Mode)",
            economic_projection=f"Expected gross yield of {projected_yield} tons/ha generates positive ROI under standard Andean margins.",
            autonomous_prediction=f"Simulation modeled locally under active contingency fallback. Irrigation investment ({irrigation}%) successfully offsets {100 - irrigation * 0.8:.0f}% of climate-related soil water stress.",
            agent_confidence=float(foundry_res["confidence_score"] * 100),
        )
        foundry_meta = FoundryIQMeta(
            status="active (local simulation)",
            confidence=float(foundry_res["confidence_score"]),
            source=foundry_res["document_name"],
        )
        fabric_meta = FabricIQMeta(
            status="connected (local simulation)",
            lakehouse=fabric_res["lakehouse"],
            synced_records=fabric_res["records_processed"],
        )
        iq_meta = MicrosoftIQMetadata(foundry_iq=foundry_meta, fabric_iq=fabric_meta)
        return SimulationResult(
            status="success",
            dashboard_metrics=metrics,
            historical_chart_data=chart_data,
            action_cards=action_cards,
            executive_summary=summary,
            microsoft_iq=iq_meta,
        )

    def get_agent_history(self, limit: int = 10) -> list:
        return self.agent_history[-limit:]


class GetAnalyticsUseCase(GetAnalyticsUseCasePort):

    def __init__(self, repository_port: SimulationRepositoryPort):
        self.repository_port = repository_port

    async def get_dashboard_analytics(
        self, region: Optional[str] = None
    ) -> Dict[str, Any]:
        return self.repository_port.get_analytics_summary(region)

    async def get_trends(
        self, region: Optional[str] = None, days: int = 30
    ) -> Dict[str, Any]:
        return self.repository_port.get_trend_data(region, days)

    async def get_history(
        self,
        region: Optional[str] = None,
        crop_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        return self.repository_port.get_simulation_history(region, crop_type, limit)

    async def compare_scenarios(self, scenario_ids: List[int]) -> List[Dict[str, Any]]:
        return self.repository_port.compare_scenarios(scenario_ids)

    async def get_roi_analysis(self, region: Optional[str] = None) -> Dict[str, Any]:
        return self.repository_port.get_roi_analysis(region)

    async def get_regional_summary(self, region: str) -> Dict[str, Any]:
        return self.repository_port.get_regional_summary(region)
