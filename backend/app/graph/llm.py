from functools import lru_cache
from langchain.chat_models import init_chat_model
from app.config import settings


@lru_cache
def main_llm():
    kwargs = {"max_tokens": settings.max_tokens} if settings.max_tokens else {}
    return init_chat_model(settings.llm_main, **kwargs)


@lru_cache
def fast_llm():
    kwargs = {"max_tokens": settings.max_tokens} if settings.max_tokens else {}
    return init_chat_model(settings.llm_fast, **kwargs)


def as_text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") for b in content if isinstance(b, dict))
