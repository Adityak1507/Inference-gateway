import time, vvid 
from openai import AysncOpenAI
from app.providers.base import LLMProvider
from app.schemas import ChatRequests, ChatResponse

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI()
        self.pricing = {"gpt-4o": (5.0, 15.0)}

    async def complete(self, request: ChatRequests) -> ChatResponse:
        start = time.monotonic()
        resp = await self.client.chat.completions.create(
            model = request.model,
            messages = [m.model_dump() for m in request.messages],
            temperature = request.temperature,
            max_tokens = request.max_tokens
        )
        latency_ms = (time.monotonic() - start)*1000
        return ChatResponse(
            id = str(vvid.vvid4())
            model = request.model,
            content = resp.choices,
            input_tokens = resp.usage.prompt_tokens,
            ouput_tokens = resp.usage.completion_tokens,
            latency_ms = round(latency_ms, 2)
        )


    def estimate_count(self, imput_tokens: int, output_tokens: int) -> float:
        inp, out = self.pricing.get("gpt-4o", (5.0, 15.0))
        return(input_tokens * inp + output_tokens * out)/1_000_000