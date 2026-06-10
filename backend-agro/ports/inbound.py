from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from domain.entities import SimulationResult


class AnalyzeCropUseCasePort(ABC):

    @abstractmethod
    async def orchestrate(
        self,
        region: str,
        crop_type: str,
        user_description: str,
        irrigation: float,
        shift: float,
        fertilizer: float,
    ) -> SimulationResult:
        pass

    @abstractmethod
    def get_agent_history(self, limit: int = 10) -> list:
        pass


class GetAnalyticsUseCasePort(ABC):

    @abstractmethod
    async def get_dashboard_analytics(
        self, region: Optional[str] = None
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_trends(
        self, region: Optional[str] = None, days: int = 30
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_history(
        self,
        region: Optional[str] = None,
        crop_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def compare_scenarios(self, scenario_ids: List[int]) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def get_roi_analysis(self, region: Optional[str] = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def get_regional_summary(self, region: str) -> Dict[str, Any]:
        pass
