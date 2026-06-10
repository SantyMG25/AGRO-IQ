from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class SimulationRepositoryPort(ABC):

    @abstractmethod
    def save_simulation(self, simulation_data: dict) -> Any:
        pass

    @abstractmethod
    def get_simulation_history(
        self,
        region: Optional[str] = None,
        crop_type: Optional[str] = None,
        limit: int = 50,
    ) -> list:
        pass

    @abstractmethod
    def get_analytics_summary(self, region: Optional[str] = None) -> dict:
        pass

    @abstractmethod
    def get_trend_data(self, region: Optional[str] = None, days: int = 30) -> dict:
        pass

    @abstractmethod
    def compare_scenarios(self, scenario_ids: List[int]) -> list:
        pass

    @abstractmethod
    def get_roi_analysis(self, region: Optional[str] = None) -> dict:
        pass

    @abstractmethod
    def get_regional_summary(self, region: str) -> dict:
        pass


class MicrosoftIQPort(ABC):

    @abstractmethod
    async def query_foundry_iq(self, region: str, query: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_fabric_telemetry(self, region: str) -> Dict[str, Any]:
        pass


class LLMReasoningPort(ABC):

    @abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        response_format: Optional[Dict[str, str]] = None,
        temperature: float = 0.3,
    ) -> str:
        pass
