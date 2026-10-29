"""Gemini access. Step 3: basic retries."""

import time
from dataclasses import dataclass

from google import genai
from google.genai import errors, types

from clauselens.config import Settings


RETRYABLE_CODES = {429, 500, 503, 504}


class EmptyResponseError(Exception):
    """Gemini returned no text."""


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LLMResult:
    """Everything we keep from one Gemini call."""
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    thought_tokens: int
    latency_s: float


# ---------------------------------------------------------------------------
# Client setup
# ---------------------------------------------------------------------------

def make_client(settings):
    """Build a Gemini client using the API key from settings."""
    http_options = types.HttpOptions(
        timeout=int(settings.request_timeout_s * 1000),
        retry_options=types.HttpRetryOptions(attempts=1),
    )

    return genai.Client(
        api_key=settings.gemini_api_key.get_secret_value(),
        http_options=http_options,
    )


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_gemini(
    client: genai.Client,
    model: str,
    prompt: str,
    system_instruction: str | None = None,
) -> LLMResult:
    """Send one prompt to Gemini and return the result."""

    request_args = {}

    if system_instruction is not None:
        request_args["config"] = types.GenerateContentConfig(
            system_instruction=system_instruction
        )

    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        **request_args,
    )

    latency_s = time.perf_counter() - start_time

    # Reject empty responses instead of treating them as successful.
    if not response.text:
        candidates = response.candidates or []
        finish_reason = (
            candidates[0].finish_reason if candidates else "unknown"
        )
        raise EmptyResponseError(
            f"Gemini returned no text. Finish reason: {finish_reason}"
        )

    usage = response.usage_metadata

    input_tokens = (
        getattr(usage, "prompt_token_count", None) or 0
    ) if usage else 0

    output_tokens = (
        getattr(usage, "candidates_token_count", None) or 0
    ) if usage else 0

    thought_tokens = (
        getattr(usage, "thoughts_token_count", None) or 0
    ) if usage else 0

    return LLMResult(
        text=response.text,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        thought_tokens=thought_tokens,
        latency_s=latency_s,
    )


# ---------------------------------------------------------------------------
# Retry logic
# ---------------------------------------------------------------------------

def call_with_retry(client, settings, model, prompt, system_instruction=None):
    """Retry temporary Gemini API errors with increasing waits."""

    for attempt in range(settings.max_retries + 1):
        try:
            return call_gemini(
                client,
                model,
                prompt,
                system_instruction,
            )

        except errors.APIError as exc:
            # Stop if the error is not retryable or attempts are exhausted.
            if (
                exc.code not in RETRYABLE_CODES
                or attempt == settings.max_retries
            ):
                raise

            # Wait 2, 4, 8... seconds, respecting the configured maximum.
            wait_seconds = min(
                settings.retry_max_wait_s,
                settings.retry_base_wait_s * (2 ** attempt),
            )

            time.sleep(wait_seconds)

            

    raise AssertionError("Retry loop exited unexpectedly")



# ---------------------------------------------------------------------------
# Fallback logic
# ---------------------------------------------------------------------------

def _should_fall_back(exc):
    """Decide whether the primary model failure justifies trying the backup."""

    # A 404 means the requested model was not found.
    # Retrying the same model will not fix a wrong model name.
    # Retryable errors are also eligible here, but only after
    # call_with_retry() has already exhausted its attempts.
    return exc.code == 404 or exc.code in RETRYABLE_CODES


def call_with_fallback(client, settings, prompt, system_instruction=None):
    """Try the primary model first, then use the backup when appropriate."""

    try:
        # First, call the primary model.
        # call_with_retry() handles temporary failures for this model.
        return call_with_retry(
            client,
            settings,
            settings.primary_model,
            prompt,
            system_instruction,
        )

    except errors.APIError as exc:
        # If the error is not eligible for fallback, stop and pass
        # the original error to whoever called this function.
        if not _should_fall_back(exc):
            raise

        # The primary model failed. Report the reason so we can see
        # when fallback happens during development.
        print(
            f"Primary model {settings.primary_model} failed "
            f"with error {exc.code}; trying backup model."
        )

        # Try the backup model. It also gets the normal retry logic.
        # If the backup fails, its error is allowed to propagate.
        return call_with_retry(
            client,
            settings,
            settings.backup_model,
            prompt,
            system_instruction,
        )
