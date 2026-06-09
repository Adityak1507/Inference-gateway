from abc import ABC, abstractmethod
from app.schemas import ChatRequests, ChatResponse

class LLMProvider(ABC):
    @abstractmethod
    async def complete(self, request: ChatRequests) -> ChatResponse:
        pass

    @abstractmethod
    def estimate_cost(self, input_tokens: int, ouput_tokens:int) -> float:
        pass    
