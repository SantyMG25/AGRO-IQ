from datetime import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Float,
    Integer,
    DateTime,
    JSON,
    func,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from ports.outbound import SimulationRepositoryPort

DATABASE_URL = "sqlite:///./agro_iq.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class SimulationModel(Base):
    __tablename__ = "simulations"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    region = Column(String, index=True)
    crop_type = Column(String)
    irrigation_investment = Column(Float)
    planting_window_shift = Column(Float)
    fertilizer_subsidy = Column(Float)
    auditor_findings = Column(JSON)
    auditor_confidence = Column(Float)
    strategy_findings = Column(JSON)
    strategy_confidence = Column(Float)
    resilience_score = Column(Float)
    food_security_index = Column(Float)
    projected_yield = Column(Float)
    loss_mitigated = Column(Float)
    executive_summary = Column(String)
    risk_level = Column(String)


class SQLiteSimulationRepository(SimulationRepositoryPort):

    def __init__(self):
        Base.metadata.create_all(bind=engine)

    def save_simulation(self, simulation_data: dict) -> Any:
        db = SessionLocal()
        try:
            sim = SimulationModel(**simulation_data)
            db.add(sim)
            db.commit()
            db.refresh(sim)
            return sim
        finally:
            db.close()

    def get_simulation_history(
        self,
        region: Optional[str] = None,
        crop_type: Optional[str] = None,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        db = SessionLocal()
        try:
            query = db.query(SimulationModel).order_by(SimulationModel.timestamp.desc())
            if region:
                query = query.filter(SimulationModel.region == region)
            if crop_type:
                query = query.filter(SimulationModel.crop_type == crop_type)
            simulations = query.limit(limit).all()
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

    def get_analytics_summary(self, region: Optional[str] = None) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            query = db.query(SimulationModel)
            if region:
                query = query.filter(SimulationModel.region == region)
            simulations = query.all()
            if not simulations:
                return {
                    "total_simulations": 0,
                    "avg_resilience": 0,
                    "avg_food_security": 0,
                    "avg_projected_yield": 0,
                    "risk_distribution": {"low": 0, "medium": 0, "high": 0},
                    "latest_simulation": None,
                }
            resilience_scores = [
                s.resilience_score
                for s in simulations
                if s.resilience_score is not None
            ]
            food_security = [
                s.food_security_index
                for s in simulations
                if s.food_security_index is not None
            ]
            yields = [
                s.projected_yield for s in simulations if s.projected_yield is not None
            ]
            risk_distribution = {
                "low": len([s for s in simulations if s.risk_level == "low"]),
                "medium": len([s for s in simulations if s.risk_level == "medium"]),
                "high": len([s for s in simulations if s.risk_level == "high"]),
            }
            latest_sim = (
                db.query(SimulationModel)
                .order_by(SimulationModel.timestamp.desc())
                .first()
            )
            return {
                "total_simulations": len(simulations),
                "avg_resilience": (
                    sum(resilience_scores) / len(resilience_scores)
                    if resilience_scores
                    else 0
                ),
                "avg_food_security": (
                    sum(food_security) / len(food_security) if food_security else 0
                ),
                "avg_projected_yield": sum(yields) / len(yields) if yields else 0,
                "risk_distribution": risk_distribution,
                "latest_simulation": (
                    latest_sim.timestamp.isoformat() if latest_sim else None
                ),
            }
        finally:
            db.close()

    def get_trend_data(
        self, region: Optional[str] = None, days: int = 30
    ) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            query = db.query(SimulationModel).filter(
                SimulationModel.timestamp >= func.datetime("now", f"-{days} days")
            )
            if region:
                query = query.filter(SimulationModel.region == region)
            simulations = query.order_by(SimulationModel.timestamp).all()
            trend_data = {
                "dates": [],
                "resilience": [],
                "food_security": [],
                "yield": [],
            }
            for sim in simulations:
                trend_data["dates"].append(sim.timestamp.isoformat())
                trend_data["resilience"].append(sim.resilience_score or 0)
                trend_data["food_security"].append(sim.food_security_index or 0)
                trend_data["yield"].append(sim.projected_yield or 0)
            return trend_data
        finally:
            db.close()

    def compare_scenarios(self, scenario_ids: List[int]) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            simulations = (
                db.query(SimulationModel)
                .filter(SimulationModel.id.in_(scenario_ids))
                .all()
            )
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
                    or sim.food_security_index
                    > comparison["best_food_security"]["value"]
                ):
                    comparison["best_food_security"] = {
                        "scenario_id": sim.id,
                        "value": sim.food_security_index,
                    }
            return comparison
        finally:
            db.close()

    def get_roi_analysis(self, region: Optional[str] = None) -> Dict[str, Any]:
        db = SessionLocal()
        try:
            query = db.query(SimulationModel)
            if region:
                query = query.filter(SimulationModel.region == region)
            simulations = query.all()
            if not simulations:
                return {"error": "No data available"}
            irrigation_buckets = {"low": [], "medium": [], "high": []}
            for sim in simulations:
                irr = sim.irrigation_investment
                if irr <= 30:
                    irrigation_buckets["low"].append(sim)
                elif irr <= 60:
                    irrigation_buckets["medium"].append(sim)
                else:
                    irrigation_buckets["high"].append(sim)
            analysis = {
                "low_investment": self._calculate_bucket_metrics(
                    irrigation_buckets["low"]
                ),
                "medium_investment": self._calculate_bucket_metrics(
                    irrigation_buckets["medium"]
                ),
                "high_investment": self._calculate_bucket_metrics(
                    irrigation_buckets["high"]
                ),
            }
            return analysis
        finally:
            db.close()

    def _calculate_bucket_metrics(
        self, simulations: List[SimulationModel]
    ) -> Dict[str, Any]:
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
        yields = [
            s.projected_yield for s in simulations if s.projected_yield is not None
        ]
        resilience = [
            s.resilience_score for s in simulations if s.resilience_score is not None
        ]
        food_security = [
            s.food_security_index
            for s in simulations
            if s.food_security_index is not None
        ]
        irrigation_costs = [s.irrigation_investment * 50 for s in simulations]
        avg_yield = sum(yields) / len(yields) if yields else 0
        avg_resilience = sum(resilience) / len(resilience) if resilience else 0
        avg_food_security = (
            sum(food_security) / len(food_security) if food_security else 0
        )
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

    def get_regional_summary(self, region: str) -> Dict[str, Any]:
        analytics = self.get_analytics_summary(region)
        trends = self.get_trend_data(region)
        history = self.get_simulation_history(region, limit=20)
        roi = self.get_roi_analysis(region)
        return {
            "region": region,
            "analytics": analytics,
            "trends": trends,
            "history": history,
            "roi": roi,
        }
