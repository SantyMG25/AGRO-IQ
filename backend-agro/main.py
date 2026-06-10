# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from adapters.outbound.database import SQLiteSimulationRepository
from adapters.outbound.microsoft_iq import MicrosoftIQAdapter
from adapters.outbound.llm import OpenAIReasoningAdapter
from application.use_cases import AnalyzeCropUseCase, GetAnalyticsUseCase
from api.router import create_router

repository = SQLiteSimulationRepository()
microsoft_iq = MicrosoftIQAdapter()
llm = OpenAIReasoningAdapter()

analyze_use_case = AnalyzeCropUseCase(
    repository_port=repository, microsoft_iq_port=microsoft_iq, llm_port=llm
)
analytics_use_case = GetAnalyticsUseCase(repository_port=repository)

app = FastAPI(title="AgroIQ - Multi-Agent Backend Engine (Hexagonal Architecture)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = create_router(analyze_use_case, analytics_use_case)
app.include_router(router)
