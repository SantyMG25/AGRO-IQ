import asyncio
import json
import os
from typing import Dict, Any
# pyrefly: ignore [missing-import]
from openai import AsyncOpenAI
from agents import AgentContext, AgentReport
from auditor_agent import AuditorAgent
from strategy_agent import StrategyAgent
from database import save_simulation, SessionLocal
from microsoft_iq import microsoft_iq_connector


class AgentOrchestrator:

    def __init__(self):
        self.auditor_agent = AuditorAgent()
        self.strategy_agent = StrategyAgent()
        self.agent_history = []
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "tu-key-aqui"))
        self.model_name = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")

    async def orchestrate(
        self,
        region: str,
        crop_type: str,
        user_description: str,
        irrigation: float,
        shift: float,
        fertilizer: float,
    ) -> Dict[str, Any]:
        context = AgentContext(
            region=region,
            crop_type=crop_type,
            user_description=user_description,
            irrigation_investment=irrigation,
            planting_window_shift=shift,
            fertilizer_subsidy=fertilizer,
        )
        print(f"[ORCHESTRATOR] Initializing Grounding Layer via Microsoft IQ...")
        foundry_task = microsoft_iq_connector.query_foundry_iq(
            region, f"climate risk {crop_type}"
        )
        fabric_task = microsoft_iq_connector.get_fabric_telemetry(region)
        foundry_res, fabric_res = await asyncio.gather(foundry_task, fabric_task)
        print(
            f"[ORCHESTRATOR] Knowledge retrieved from {foundry_res['document_name']}. Syncing with Lakehouse: {fabric_res['lakehouse']}."
        )
        system_prompt = "\n        Eres el Orquestador Multi-Agente Avanzado de AgroGarantia IQ. Tu objetivo es actuar en dos fases consecutivas:\n        1. AGENTE AUDITOR: Analiza los datos de los sensores, los sliders de entrada y contrasta con los manuales oficiales de la FAO recuperados de Microsoft Foundry IQ.\n        2. AGENTE ESTRATÉGICO: Evalúa la viabilidad económica y genera alertas críticas predictivas basadas en las vulnerabilidades encontradas.\n\n        DEBES responder EXCLUSIVAMENTE con un objeto JSON estructurado que contenga las métricas de impacto calculadas de forma autónoma y las recomendaciones redactadas en vivo. No uses plantillas estáticas.\n        "
        user_prompt = f"""\n        FICHA TÉCNICA DEL ESCENARIO DE SIMULACIÓN:\n        - Región de Análisis: {region}\n        - Cultivo Monitoreado: {crop_type}\n        - Contexto Operativo: {user_description}\n        \n        VARIABLES DE ENTRADA (SLIDERS):\n        - Inversión en Infraestructura Hídrica: {irrigation}%\n        - Desfase Calendario de Siembra: {shift} Semanas\n        - Subsidio de Fertilizantes: {fertilizer}%\n\n        CONTEXTO INTEGRADO MICROSOFT FOUNDRY IQ (RAG - MANUAL DE LA FAO):\n        - Origen del Documento: {foundry_res['source_document']}\n        - Confianza del Conocimiento: {foundry_res['confidence_score'] * 100}%\n        - Datos de Soporte Indexados: {json.dumps(foundry_res['retrieved_metadata'])}\n\n        TELEMETRÍA MICROSOFT FABRIC IQ (LAKEHOUSE DATALAKE):\n        - Origen: {fabric_res['lakehouse']} -> Tabla: {fabric_res['table_source']}\n        - Esquema de Datos Analíticos: {json.dumps(fabric_res['data_schema'])}\n        - Registros Históricos Procesados: {fabric_res['records_processed']}\n\n        REGLAS DE NEGOCIO PARA EL MODELO GENERATIVO:\n        1. Calcula el 'resilience_score' (0-100) y 'food_security_index' (0-100) basándote de verdad en los impactos cruzados. Si la inversión en riego es baja (<30%) y el desfase de semanas expone el cultivo al pico de heladas indicadas por la FAO, penaliza fuertemente los índices.\n        2. Proyecta las toneladas de rendimiento ('projected_yield_tons') y la pérdida mitigada en dólares ('economic_loss_prevented_usd').\n        3. Redacta las descripciones de las tarjetas ('action_cards') con lenguaje natural altamente profesional, técnico, corporativo y 100% enfocado en el impacto ESG de este escenario específico.\n        4. Construye el análisis de riesgo mensual ('historical_chart_data') para Julio, Agosto y Septiembre, modificando los valores mitigados según la inversión.\n\n        DEBES devolver estrictamente este formato JSON:\n        {{\n            "dashboard_metrics": {{\n                "food_security_index": int,\n                "projected_yield_tons": float,\n                "economic_loss_prevented_usd": int,\n                "resilience_score": int\n            }},\n            "historical_chart_data": [\n                {{"month": "Jul", "base_risk": int, "mitigated_risk": int, "agent_insight": "string"}},\n                {{"month": "Ago", "base_risk": int, "mitigated_risk": int, "agent_insight": "string"}},\n                {{"month": "Sep", "base_risk": int, "mitigated_risk": int, "agent_insight": "string"}}\n            ],\n            "action_cards": [\n                {{"id": "1", "title": "Water Resource Optimization", "description": "string", "agent_reasoning": "string", "visual_indicator": "emerald|amber|red", "resilience_contribution": "string"}},\n                {{"id": "2", "title": "Strategic Recommendation", "description": "string", "executive_priority": "string", "visual_indicator": "emerald|amber", "decision_triggers": ["string"]}},\n                {{"id": "3", "title": "Critical Alert", "description": "string", "visual_indicator": "red", "agent_source": "string"}}\n            ],\n            "executive_summary": {{\n                "scenario_viability": "string",\n                "economic_projection": "string",\n                "autonomous_prediction": "string"\n            }}\n        }}\n        """
        try:
            print(
                f"[ORCHESTRATOR] Dispatching generative analysis to LLM ({self.model_name})..."
            )
            response = await self.client.chat.completions.create(
                model=self.model_name,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
            )
            generated_json = json.loads(response.choices[0].message.content)
            print(
                "[ORCHESTRATOR] Multi-Agent autonomous inference successfully generated."
            )
            generated_json["status"] = "success"
            generated_json["microsoft_iq"] = {
                "foundry_iq": {
                    "status": "active",
                    "confidence": foundry_res["confidence_score"],
                    "source": foundry_res["document_name"],
                },
                "fabric_iq": {
                    "status": "connected",
                    "lakehouse": fabric_res["lakehouse"],
                    "synced_records": fabric_res["records_processed"],
                },
            }
            generated_json["executive_summary"]["agent_confidence"] = float(
                foundry_res["confidence_score"] * 100
            )
            auditor_report = AgentReport(
                confidence=foundry_res["confidence_score"],
                findings=foundry_res["retrieved_metadata"],
                raw_analysis="Inferencia Basada en Foundry IQ",
            )
            strategy_report = AgentReport(
                confidence=0.92,
                findings=generated_json["executive_summary"],
                raw_analysis=generated_json["executive_summary"][
                    "autonomous_prediction"
                ],
            )
            self._save_to_database(
                context, auditor_report, strategy_report, generated_json
            )
            self.agent_history.append(
                {"context": context, "aggregated": generated_json}
            )
            return generated_json
        except Exception as e:
            print(f"[ERROR CRÍTICO ORQUESTADOR]: {str(e)}")
            return {
                "status": "error",
                "message": f"Falló la inferencia generativa real: {str(e)}",
            }

    def get_agent_history(self, limit: int = 10) -> list:
        return self.agent_history[-limit:]

    def _save_to_database(
        self,
        context: AgentContext,
        auditor_report: AgentReport,
        strategy_report: AgentReport,
        aggregated: Dict[str, Any],
    ) -> None:
        try:
            db = SessionLocal()
            metrics = aggregated["dashboard_metrics"]
            simulation_data = {
                "region": context.region,
                "crop_type": context.crop_type,
                "irrigation_investment": context.irrigation_investment,
                "planting_window_shift": context.planting_window_shift,
                "fertilizer_subsidy": context.fertilizer_subsidy,
                "auditor_findings": json.dumps(auditor_report.findings),
                "auditor_confidence": auditor_report.confidence,
                "strategy_findings": json.dumps(aggregated["executive_summary"]),
                "strategy_confidence": strategy_report.confidence,
                "resilience_score": metrics["resilience_score"],
                "food_security_index": metrics["food_security_index"],
                "projected_yield": metrics["projected_yield_tons"],
                "loss_mitigated": metrics["economic_loss_prevented_usd"],
                "executive_summary": aggregated["executive_summary"][
                    "autonomous_prediction"
                ],
                "risk_level": (
                    "low"
                    if metrics["resilience_score"] >= 75
                    else "medium" if metrics["resilience_score"] >= 50 else "high"
                ),
            }
            save_simulation(db, simulation_data)
            print(f"[DATABASE] Simulación persistida con éxito en agro_iq.db.")
        except Exception as e:
            print(f"[DATABASE ERROR] Error al guardar simulación: {e}")
        finally:
            db.close()
