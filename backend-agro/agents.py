from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, List


@dataclass
class AgentContext:
    region: str
    crop_type: str
    user_description: str
    irrigation_investment: float
    planting_window_shift: float
    fertilizer_subsidy: float


@dataclass
class AgentReport:
    agent_name: str
    role: str
    findings: Dict[str, Any]
    confidence: float
    raw_analysis: str


class Agent(ABC):

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role

    @abstractmethod
    async def analyze(self, context: AgentContext) -> AgentReport:
        pass

    def _calculate_risk_score(self, irrigation: float, shift: float) -> int:
        base_risk = 70
        irrigation_reduction = irrigation / 100 * 40
        shift_penalty = abs(shift) * 5
        return max(0, min(100, int(base_risk - irrigation_reduction + shift_penalty)))
