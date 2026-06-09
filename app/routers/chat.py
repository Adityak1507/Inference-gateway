from fastapi import APIRouter, Depends
from app.schemas import ChatRequest, ChatResponse
from app.auth import get_current_user
from app.providers.openai import OpenAIProvider
from app.models import RequestLog
import time

router = APIRouter()
provider = OpenAIProvider()

@router.post("/v1/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, user_id: str = Depends(get_current_user), db=Depends(get_db)):
    response = await provider.complete(request)
    cost = provider.estimate_cost(response.input_tokens, response.output_tokens)
    
    # Log to Postgres
    log = RequestLog(
        user_id=user_id,
        model=response.model,
        provider_used=response.provider_used,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        latency_ms=response.latency_ms,
        cost_usd=cost,
    )
    db.add(log)
    await db.commit()
    
    return response