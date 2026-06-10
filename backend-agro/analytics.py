from typing import Dict, List, Optional
from database import (
    get_db,
    get_analytics_summary,
    get_simulation_history,
    get_trend_data,
    SessionLocal,
)
from sqlalchemy.orm import Session


def get_dashboard_analytics(region: Optional[str] = None) -> Dict:
    db = SessionLocal()
    try:
        return get_analytics_summary(db, region)
    finally:
        db.close()


def get_trends(region: Optional[str] = None, days: int = 30) -> Dict:
    db = SessionLocal()
    try:
        return get_trend_data(db, region, days)
    finally:
        db.close()


def get_history(
    region: Optional[str] = None, crop_type: Optional[str] = None, limit: int = 50
) -> List[Dict]:
    db = SessionLocal()
    try:
        simulations = get_simulation_history(db, region, crop_type, limit)
        return [
            {
                "id": sim.id,
                "timestamp": sim.timestamp.isoformat(),
                "region": sim.region,
                "crop_type": sim.crop_type,
                "irrigation_investment": sim.irrigation_investment,
                "planting_window_shift": sim.planting_window_shift,
                "resilience_score": sim.resilience_score,
                "food_security_index": sim.food_security_index,
                "projected_yield": sim.projected_yield,
                "loss_mitigated": sim.loss_mitigated,
                "risk_level": sim.risk_level,
            }
            for sim in simulations
        ]
    finally:
        db.close()


def compare_scenarios(scenario_ids: List[int]) -> Dict:
    db = SessionLocal()
    try:
        from database import Simulation

        simulations = db.query(Simulation).filter(Simulation.id.in_(scenario_ids)).all()
        if not simulations:
            return {"error": "No simulations found"}
        comparison = {
            "scenarios": [],
            "best_resilience": None,
            "best_yield": None,
            "best_food_security": None,
            "cost_analysis": [],
        }
        for sim in simulations:
            scenario_data = {
                "id": sim.id,
                "timestamp": sim.timestamp.isoformat(),
                "irrigation": sim.irrigation_investment,
                "shift": sim.planting_window_shift,
                "fertilizer": sim.fertilizer_subsidy,
                "resilience": sim.resilience_score,
                "yield": sim.projected_yield,
                "food_security": sim.food_security_index,
                "loss_prevented": sim.loss_mitigated,
                "risk": sim.risk_level,
            }
            comparison["scenarios"].append(scenario_data)
            if (
                not comparison["best_resilience"]
                or sim.resilience_score > comparison["best_resilience"]["score"]
            ):
                comparison["best_resilience"] = {
                    "scenario_id": sim.id,
                    "score": sim.resilience_score,
                }
            if (
                not comparison["best_yield"]
                or sim.projected_yield > comparison["best_yield"]["value"]
            ):
                comparison["best_yield"] = {
                    "scenario_id": sim.id,
                    "value": sim.projected_yield,
                }
            if (
                not comparison["best_food_security"]
                or sim.food_security_index > comparison["best_food_security"]["value"]
            ):
                comparison["best_food_security"] = {
                    "scenario_id": sim.id,
                    "value": sim.food_security_index,
                }
        return comparison
    finally:
        db.close()


def get_roi_analysis(region: Optional[str] = None) -> Dict:
    db = SessionLocal()
    try:
        from database import Simulation

        query = db.query(Simulation)
        if region:
            query = query.filter(Simulation.region == region)
        simulations = query.all()
        if not simulations:
            return {"error": "No data available"}
        irrigation_buckets = {
            "low": {"0-30": []},
            "medium": {"30-60": []},
            "high": {"60-100": []},
        }
        for sim in simulations:
            irr = sim.irrigation_investment
            if irr <= 30:
                irrigation_buckets["low"]["0-30"].append(sim)
            elif irr <= 60:
                irrigation_buckets["medium"]["30-60"].append(sim)
            else:
                irrigation_buckets["high"]["60-100"].append(sim)
        analysis = {
            "low_investment": _calculate_bucket_metrics(
                irrigation_buckets["low"]["0-30"]
            ),
            "medium_investment": _calculate_bucket_metrics(
                irrigation_buckets["medium"]["30-60"]
            ),
            "high_investment": _calculate_bucket_metrics(
                irrigation_buckets["high"]["60-100"]
            ),
        }
        return analysis
    finally:
        db.close()


def _calculate_bucket_metrics(simulations: List) -> Dict:
    if not simulations:
        return {
            "count": 0,
            "avg_yield": 0,
            "avg_resilience": 0,
            "avg_food_security": 0,
            "avg_investment_cost": 0,
            "avg_roi": 0,
        }
    count = len(simulations)
    yields = [s.projected_yield for s in simulations if s.projected_yield]
    resilience = [s.resilience_score for s in simulations if s.resilience_score]
    food_security = [
        s.food_security_index for s in simulations if s.food_security_index
    ]
    irrigation_costs = [s.irrigation_investment * 50 for s in simulations]
    avg_yield = sum(yields) / len(yields) if yields else 0
    avg_resilience = sum(resilience) / len(resilience) if resilience else 0
    avg_food_security = sum(food_security) / len(food_security) if food_security else 0
    avg_cost = sum(irrigation_costs) / count if count else 0
    avg_revenue = avg_yield * 200
    avg_roi = (avg_revenue - avg_cost) / avg_cost * 100 if avg_cost > 0 else 0
    return {
        "count": count,
        "avg_yield": round(avg_yield, 2),
        "avg_resilience": round(avg_resilience, 1),
        "avg_food_security": round(avg_food_security, 1),
        "avg_investment_cost": round(avg_cost, 2),
        "avg_roi": round(avg_roi, 1),
    }


def get_regional_summary(region: str) -> Dict:
    db = SessionLocal()
    try:
        analytics = get_dashboard_analytics(region)
        trends = get_trends(region)
        history = get_history(region, limit=20)
        roi = get_roi_analysis(region)
        return {
            "region": region,
            "analytics": analytics,
            "trends": trends,
            "recent_simulations": history,
            "roi_analysis": roi,
        }
    finally:
        db.close()
