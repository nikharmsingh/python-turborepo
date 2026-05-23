from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from llm.streaming import stream_text_async

router = APIRouter()


class ChatRequest(BaseModel):
    prompt: str
    model: str = "claude-sonnet-4-6"
    system: str = "You are a helpful assistant."


@router.post("/stream")
async def chat_stream(req: ChatRequest) -> StreamingResponse:
    async def _generate():
        async for chunk in stream_text_async(req.prompt, model=req.model, system=req.system):
            yield chunk

    return StreamingResponse(_generate(), media_type="text/plain")
