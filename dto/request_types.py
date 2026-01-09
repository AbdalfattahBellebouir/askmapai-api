from pydantic import BaseModel

class AskMapAIRequest(BaseModel):
    isDeepThinking: bool
    prompt: str