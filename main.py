import json
import os
from fastapi import FastAPI, Request
from dto.request_types import AskMapAIRequest
from dto.response_types import AskMapAIResponse
from services.get_answer import get_answer_deepseek
from startup.env_startup import setup_env
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = setup_env()

app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["*"] to allow all
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],
)


@app.post("/askmapai")
async def askmapai(request: Request, req: AskMapAIRequest) -> AskMapAIResponse:
    import time
    start_time = time.time()
    locations, answer = get_answer_deepseek(client=client, isDeepThinking=req.isDeepThinking, prompt=req.prompt)
    with open(os.getenv('LOG_FILE'), "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "Timestamp": datetime.utcnow().isoformat(),
            "IP": request.client.host,
            "Prompt": req.prompt,
            "isDeepThinking": req.isDeepThinking,
            "ElapsedTimeInSeconds": time.time() - start_time,
            "locations": json.dumps([u.__dict__ for u in locations]),
            "answer": answer
        })+"\n")
    

    return AskMapAIResponse(locations=locations, answer=answer)

print("Api is up and ready to work :)")