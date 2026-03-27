"""Neo Says API — because even APIs deserve attitude."""

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from typing import List, Optional

from neo_says.quotes import (
    get_quote,
    get_quote_of_the_day,
    get_categories,
    get_tags,
    SUPPORTED_LANGS,
)


limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Neo Says API",
    description=(
        "You wanted wisdom? Fine. Here's an API that dispenses unsolicited "
        "truth bombs, mass cynicism, and the occasional mass enlightenment. "
        "Neo doesn't sugarcoat. Neo doesn't care about your feelings. "
        "Neo just tells it like it is.\n\n"
        "Rate limited to 15 req/min because even Neo needs a breather."
    ),
    version="7.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Response Models ---

class QuoteResponse(BaseModel):
    """A single quote served with Neo's signature disdain."""

    text: str = Field(..., description="The quote text. You're welcome.")
    category: str = Field(..., description="Category this quote belongs to.")
    lang: str = Field(..., description="Language code of the quote.")


class CategoriesResponse(BaseModel):
    """List of categories, because you need labels for everything."""

    categories: List[str]


class TagsResponse(BaseModel):
    """List of tags. Yes, we tag things. Deal with it."""

    tags: List[str]


class HealthResponse(BaseModel):
    """Health check. Neo is always fine. Stop asking."""

    status: str
    message: str


class WelcomeResponse(BaseModel):
    """Welcome message. Don't get used to the hospitality."""

    message: str
    docs: str
    endpoints: List[str]


# --- Helper ---

def _validate_lang(lang: Optional[str]) -> Optional[str]:
    """Validate language parameter. Returns None if valid or not provided."""
    if lang is not None and lang not in SUPPORTED_LANGS:
        return lang  # return the invalid lang for error message
    return None


def _resolve_lang(lang: Optional[str]) -> str:
    """Resolve lang param to a concrete language code."""
    return lang if lang else "en"


# --- Endpoints ---

@app.get(
    "/",
    response_model=WelcomeResponse,
    summary="Welcome to Neo's domain",
    description="You found the front door. Congratulations. Here's a map so you don't get lost.",
)
@limiter.limit("15/minute")
def root(request: Request):
    return WelcomeResponse(
        message="Welcome to Neo Says API. I'd say 'make yourself at home' but I'd rather you didn't.",
        docs="/docs",
        endpoints=[
            "GET /quote",
            "GET /quote/today",
            "GET /quote/{category}",
            "GET /categories",
            "GET /tags",
            "GET /health",
        ],
    )


@app.get(
    "/quote",
    response_model=QuoteResponse,
    summary="Get a random quote",
    description="Fetch a random quote. Optionally filter by category, tag, or language. Neo picks. You receive.",
)
@limiter.limit("15/minute")
def random_quote(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by category"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    lang: Optional[str] = Query(None, description=f"Language: {', '.join(SUPPORTED_LANGS)}"),
):
    invalid = _validate_lang(lang)
    if invalid:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Language '{invalid}' not supported. Try one of {SUPPORTED_LANGS}. Neo speaks many languages, but not that one."
            },
        )

    resolved_lang = _resolve_lang(lang)

    if category and category not in get_categories(resolved_lang):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Category '{category}' doesn't exist. Much like your taste. Try GET /categories for valid options."
            },
        )

    text, cat = get_quote(category=category, tag=tag, lang=resolved_lang)
    return QuoteResponse(text=text, category=cat, lang=resolved_lang)


@app.get(
    "/quote/today",
    response_model=QuoteResponse,
    summary="Quote of the day",
    description="Today's handpicked quote. Same quote all day because consistency is a virtue you clearly lack.",
)
@limiter.limit("15/minute")
def quote_of_the_day(
    request: Request,
    lang: Optional[str] = Query(None, description=f"Language: {', '.join(SUPPORTED_LANGS)}"),
):
    invalid = _validate_lang(lang)
    if invalid:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Language '{invalid}' not supported. Try one of {SUPPORTED_LANGS}. Neo speaks many languages, but not that one."
            },
        )

    resolved_lang = _resolve_lang(lang)
    text, cat = get_quote_of_the_day(lang=resolved_lang)
    return QuoteResponse(text=text, category=cat, lang=resolved_lang)


@app.get(
    "/quote/{category}",
    response_model=QuoteResponse,
    summary="Random quote from a category",
    description="Get a random quote from a specific category. At least you're trying to be organized.",
)
@limiter.limit("15/minute")
def quote_by_category(
    request: Request,
    category: str,
    lang: Optional[str] = Query(None, description=f"Language: {', '.join(SUPPORTED_LANGS)}"),
):
    invalid = _validate_lang(lang)
    if invalid:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Language '{invalid}' not supported. Try one of {SUPPORTED_LANGS}. Neo speaks many languages, but not that one."
            },
        )

    resolved_lang = _resolve_lang(lang)

    if category not in get_categories(resolved_lang):
        return JSONResponse(
            status_code=404,
            content={
                "detail": f"Category '{category}' not found. Shocking, I know. Try GET /categories to see what actually exists."
            },
        )

    text, cat = get_quote(category=category, lang=resolved_lang)
    return QuoteResponse(text=text, category=cat, lang=resolved_lang)


@app.get(
    "/categories",
    response_model=CategoriesResponse,
    summary="List all categories",
    description="Get all available quote categories. So you can pretend you have preferences.",
)
@limiter.limit("15/minute")
def list_categories(
    request: Request,
    lang: Optional[str] = Query(None, description=f"Language: {', '.join(SUPPORTED_LANGS)}"),
):
    invalid = _validate_lang(lang)
    if invalid:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Language '{invalid}' not supported. Try one of {SUPPORTED_LANGS}."
            },
        )

    resolved_lang = _resolve_lang(lang)
    return CategoriesResponse(categories=get_categories(resolved_lang))


@app.get(
    "/tags",
    response_model=TagsResponse,
    summary="List all tags",
    description="Get all available tags. For the taxonomically obsessed.",
)
@limiter.limit("15/minute")
def list_tags(
    request: Request,
    lang: Optional[str] = Query(None, description=f"Language: {', '.join(SUPPORTED_LANGS)}"),
):
    invalid = _validate_lang(lang)
    if invalid:
        return JSONResponse(
            status_code=400,
            content={
                "detail": f"Language '{invalid}' not supported. Try one of {SUPPORTED_LANGS}."
            },
        )

    resolved_lang = _resolve_lang(lang)
    return TagsResponse(tags=get_tags(resolved_lang))


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if Neo is alive. Spoiler: Neo is always alive.",
)
@limiter.limit("15/minute")
def health_check(request: Request):
    return HealthResponse(
        status="ok",
        message="Neo is alive, mass cynical, and mass ready to judge your life choices.",
    )
