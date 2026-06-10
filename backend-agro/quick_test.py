import asyncio
import sys
from orchestrator import AgentOrchestrator


async def test_agents():
    print("🚀 Starting Agent Test...")
    print("-" * 50)
    orchestrator = AgentOrchestrator()
    try:
        print("✓ Orchestrator initialized")
        result = await orchestrator.orchestrate(
            region="Global Andean Region",
            crop_type="Subsistence Corn",
            user_description="Quick test",
            irrigation=30,
            shift=0,
            fertilizer=50,
        )
        print("✓ Orchestration completed successfully!")
        print("\n📊 RESULT SUMMARY:")
        print(f"  - Status: {result.get('status')}")
        print(
            f"  - Auditor Confidence: {result['agent_pipeline']['auditor']['confidence']}"
        )
        print(
            f"  - Strategy Confidence: {result['agent_pipeline']['strategy']['confidence']}"
        )
        print(
            f"  - Resilience Score: {result['dashboard_metrics']['resilience_score']}"
        )
        print(
            f"  - Food Security: {result['dashboard_metrics']['food_security_index']}"
        )
        print(f"  - Yield: {result['dashboard_metrics']['projected_yield_tons']} tons")
        print("\n✅ Agent system is WORKING!")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(test_agents())
