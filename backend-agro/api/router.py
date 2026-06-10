from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from domain.entities import AnalysisRequest, SimulationResult
from ports.inbound import AnalyzeCropUseCasePort, GetAnalyticsUseCasePort


def create_router(
    analyze_use_case: AnalyzeCropUseCasePort,
    analytics_use_case: GetAnalyticsUseCasePort,
) -> APIRouter:
    router = APIRouter()

    @router.post("/api/analyze", response_model=SimulationResult)
    async def analyze_crop_security(request: AnalysisRequest):
        try:
            result = await analyze_use_case.orchestrate(
                region=request.region,
                crop_type=request.crop_type,
                user_description=request.user_description,
                irrigation=request.variables.irrigation_investment,
                shift=request.variables.planting_window_shift,
                fertilizer=request.variables.fertilizer_subsidy,
            )
            return result
        except Exception as e:
            print(f"[ERROR] Web controller analyze failed: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"Orchestration error: {str(e)}"
            )

    @router.get("/api/history")
    async def get_simulation_history(limit: int = 10):
        try:
            history = analyze_use_case.get_agent_history(limit)
            return {
                "total_simulations": len(history),
                "recent_simulations": len(history) if len(history) <= limit else limit,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/api/analytics/dashboard")
    async def analytics_dashboard(region: Optional[str] = None):
        try:
            return await analytics_use_case.get_dashboard_analytics(region)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/api/analytics/trends")
    async def analytics_trends(region: Optional[str] = None, days: int = 30):
        try:
            return await analytics_use_case.get_trends(region, days)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/api/analytics/history")
    async def analytics_history(
        region: Optional[str] = None, crop_type: Optional[str] = None, limit: int = 50
    ):
        try:
            return await analytics_use_case.get_history(region, crop_type, limit)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/api/analytics/compare")
    async def analytics_compare(scenario_ids: List[int]):
        try:
            return await analytics_use_case.compare_scenarios(scenario_ids)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/api/analytics/roi")
    async def analytics_roi(region: Optional[str] = None):
        try:
            return await analytics_use_case.get_roi_analysis(region)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/api/analytics/regional/{region}")
    async def analytics_regional(region: str):
        try:
            return await analytics_use_case.get_regional_summary(region)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "agents": {"auditor": "ready", "strategy": "ready"},
            "orchestrator": "operational",
        }

    return router
