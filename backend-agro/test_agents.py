import asyncio
from orchestrator import AgentOrchestrator


async def main():
    orchestrator = AgentOrchestrator()
    print("[TEST] Starting agent orchestration test...")
    print("=" * 60)
    result = await orchestrator.orchestrate(
        region="Global Andean Region",
        crop_type="Subsistence Corn",
        user_description="Test simulation",
        irrigation=60,
        shift=1,
        fertilizer=50,
    )
    print(f"Status: {result['status']}")
    print(
        f"Auditor Confidence: {result['agent_pipeline']['auditor']['confidence']:.0%}"
    )
    print(
        f"Strategy Confidence: {result['agent_pipeline']['strategy']['confidence']:.0%}"
    )
    print(f"\nDashboard Metrics:")
    print(
        f"  - Food Security Index: {result['dashboard_metrics']['food_security_index']}%"
    )
    print(
        f"  - Projected Yield: {result['dashboard_metrics']['projected_yield_tons']} tons"
    )
    print(
        f"  - Loss Mitigated: ${result['dashboard_metrics']['economic_loss_prevented_usd']}"
    )
    print(
        f"  - Resilience Score: {result['dashboard_metrics']['resilience_score']}/100"
    )
    print(f"\nAgent Pipeline:")
    print(f"  - Auditor Agent: {result['agent_pipeline']['auditor']['status']}")
    print(f"  - Strategy Agent: {result['agent_pipeline']['strategy']['status']}")
    if "executive_summary" in result:
        print(f"\nExecutive Summary Generated: Yes")
        print(
            f"Agent Confidence: {result['executive_summary']['agent_confidence']:.0%}"
        )
    print("\n[TEST] ✓ Agent orchestration completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
