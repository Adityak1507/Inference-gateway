from pydantic import Basemodel
from typing import Literal

class Message(Basemodel):
    role: Litreal["System", "User", "Assistant"]
    content: str

class ChatRequests(Basemodel):
    model: str
    messages: List[Message] 
    temperature: float = 0.7
    max_tokens = int = 1000
    stream: bool = False

class ChatResponse(Basemodel):
    id: str
    model: str
    content: str
    provider_used: str
    input_tokens: int
    ouput_tokens: int
    latency_ms: float      
