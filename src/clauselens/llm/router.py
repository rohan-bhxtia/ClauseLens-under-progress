"""Gemini access. Step 2: one basic API call."""

import time
from dataclasses import dataclass
from google import genai
from clauselens.config import Settings
from google.genai import types


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LLMResult:
    """Everything we keep from one Gemini call."""
    text: str             # the model's reply
    model: str            # which model answered
    input_tokens: int     # tokens in our prompt
    output_tokens: int    # tokens in the visible reply
    thought_tokens: int   # tokens the model spent "thinking" (not shown in text)
    latency_s: float      # how long the call took, in seconds


# ---------------------------------------------------------------------------
# Client setup
# ---------------------------------------------------------------------------

def make_client(settings):
    """Build a Gemini client using the API key from settings."""
    client = genai.Client(
        api_key=settings.gemini_api_key.get_secret_value()
    )
    return client


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_gemini(
    client: genai.Client,
    model: str,
    prompt: str,
    system_instruction: str | None = None,) -> LLMResult:
    """Send one prompt to Gemini and return the result."""

    # Start timing the call
    start_time = time.perf_counter()

    # Optional settings: only send a config if there is a system instruction
    request_args = {}

    if system_instruction is not None:
        request_args["config"] = types.GenerateContentConfig(
            system_instruction=system_instruction
        )

    # Send the prompt to Gemini
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        **request_args
    )

    # Read token counts (default to 0 if Gemini leaves any out)
    usage = response.usage_metadata

    input_tokens = (getattr(usage, "prompt_token_count", None) or 0) if usage else 0
    output_tokens = (getattr(usage, "candidates_token_count", None) or 0) if usage else 0
    thought_tokens = (getattr(usage, "thoughts_token_count", None) or 0) if usage else 0

    # Stop timing
    latency_s = time.perf_counter() - start_time

    # Package everything into one result
    return LLMResult(
        text=response.text or "",
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        thought_tokens=thought_tokens,
        latency_s=latency_s,
    )
