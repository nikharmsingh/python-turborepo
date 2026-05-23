from collections.abc import AsyncGenerator, Generator
from .client import get_async_client, get_client


def stream_text(
    prompt: str,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 4096,
    system: str = "You are a helpful assistant.",
) -> Generator[str, None, None]:
    client = get_client()
    with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        yield from stream.text_stream


async def stream_text_async(
    prompt: str,
    model: str = "claude-sonnet-4-6",
    max_tokens: int = 4096,
    system: str = "You are a helpful assistant.",
) -> AsyncGenerator[str, None]:
    client = get_async_client()
    async with client.messages.stream(
        model=model,
        max_tokens=max_tokens,
        system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        async for chunk in stream.text_stream:
            yield chunk
