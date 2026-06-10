from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

DATABASE_URL = "sqlite:///./agro_iq.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Simulation(Base):
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


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_simulation(db_session, simulation_data: dict) -> Simulation:
    sim = Simulation(**simulation_data)
    db_session.add(sim)
    db_session.commit()
    db_session.refresh(sim)
    return sim


def get_simulation_history(
    db_session, region: str = None, crop_type: str = None, limit: int = 50
):
    query = db_session.query(Simulation).order_by(Simulation.timestamp.desc())
    if region:
        query = query.filter(Simulation.region == region)
    if crop_type:
        query = query.filter(Simulation.crop_type == crop_type)
    return query.limit(limit).all()


def get_analytics_summary(db_session, region: str = None) -> dict:
    query = db_session.query(Simulation)
    if region:
        query = query.filter(Simulation.region == region)
    simulations = query.all()
    if not simulations:
        return {
            "total_simulations": 0,
            "avg_resilience": 0,
            "avg_food_security": 0,
            "avg_projected_yield": 0,
            "risk_distribution": {"low": 0, "medium": 0, "high": 0},
        }
    resilience_scores = [s.resilience_score for s in simulations if s.resilience_score]
    food_security = [
        s.food_security_index for s in simulations if s.food_security_index
    ]
    yields = [s.projected_yield for s in simulations if s.projected_yield]
    risk_distribution = {
        "low": len([s for s in simulations if s.risk_level == "low"]),
        "medium": len([s for s in simulations if s.risk_level == "medium"]),
        "high": len([s for s in simulations if s.risk_level == "high"]),
    }
    return {
        "total_simulations": len(simulations),
        "avg_resilience": (
            sum(resilience_scores) / len(resilience_scores) if resilience_scores else 0
        ),
        "avg_food_security": (
            sum(food_security) / len(food_security) if food_security else 0
        ),
        "avg_projected_yield": sum(yields) / len(yields) if yields else 0,
        "risk_distribution": risk_distribution,
        "latest_simulation": simulations[0].timestamp if simulations else None,
    }


def get_trend_data(db_session, region: str = None, days: int = 30):
    from sqlalchemy import func

    query = db_session.query(Simulation).filter(
        Simulation.timestamp >= func.datetime("now", f"-{days} days")
    )
    if region:
        query = query.filter(Simulation.region == region)
    simulations = query.order_by(Simulation.timestamp).all()
    trend_data = {"dates": [], "resilience": [], "food_security": [], "yield": []}
    for sim in simulations:
        trend_data["dates"].append(sim.timestamp.isoformat())
        trend_data["resilience"].append(sim.resilience_score or 0)
        trend_data["food_security"].append(sim.food_security_index or 0)
        trend_data["yield"].append(sim.projected_yield or 0)
    return trend_data
