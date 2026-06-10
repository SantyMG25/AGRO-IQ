# pyrefly: ignore [missing-import]
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class SimulationVariables(BaseModel):
    irrigation_investment: float
    planting_window_shift: float
    fertilizer_subsidy: float


class AnalysisRequest(BaseModel):
    region: str
    crop_type: str
    user_description: str
    variables: SimulationVariables


class AgentContext(BaseModel):
    region: str
    crop_type: str
    user_description: str
    irrigation_investment: float
    planting_window_shift: float
    fertilizer_subsidy: float


class AgentReport(BaseModel):
    agent_name: str
    role: str
    findings: Dict[str, Any]
    confidence: float
    raw_analysis: str


class DashboardMetrics(BaseModel):
    food_security_index: int
    projected_yield_tons: float
    economic_loss_prevented_usd: int
    resilience_score: int


class HistoricalChartItem(BaseModel):
    month: str
    base_risk: int
    mitigated_risk: int
    agent_insight: str


class ActionCard(BaseModel):
    id: str
    title: str
    description: str
    agent_reasoning: Optional[str] = None
    visual_indicator: str
    resilience_contribution: Optional[str] = None
    executive_priority: Optional[str] = None
    decision_triggers: Optional[List[str]] = None
    agent_source: Optional[str] = None


class ExecutiveSummary(BaseModel):
    scenario_viability: str
    economic_projection: str
    autonomous_prediction: str
    agent_confidence: Optional[float] = None


class FoundryIQMeta(BaseModel):
    status: str
    confidence: float
    source: str


class FabricIQMeta(BaseModel):
    status: str
    lakehouse: str
    synced_records: int


class MicrosoftIQMetadata(BaseModel):
    foundry_iq: FoundryIQMeta
    fabric_iq: FabricIQMeta


class SimulationResult(BaseModel):
    status: str
    dashboard_metrics: DashboardMetrics
    historical_chart_data: List[HistoricalChartItem]
    action_cards: List[ActionCard]
    executive_summary: ExecutiveSummary
    microsoft_iq: Optional[MicrosoftIQMetadata] = None
    message: Optional[str] = None
