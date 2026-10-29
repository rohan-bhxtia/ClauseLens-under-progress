"""Manual tests for Gemini retry and fallback."""

from clauselens.config import get_settings
from clauselens.llm.router import (
    call_gemini,
    call_with_fallback,
    make_client,
)

settings = get_settings()
client = make_client(settings)

# Test 1: Check that the backup model works on its own.
print("--- Test 1: Backup model directly ---")
result = call_gemini(
    client,
    settings.backup_model,
    "Reply with exactly: ok",
)
print(result)

# Test 2: Normal fallback function call.
# The primary model should answer, so the backup should not be needed.
print("--- Test 2: Primary model with fallback enabled ---")
result = call_with_fallback(
    client,
    settings,
    "Reply with exactly: ok",
)
print(result)

# Test 3: Force the primary model to be invalid.
# The router should detect the 404 and try the backup model.
print("--- Test 3: Force fallback to backup ---")
settings.primary_model = "not-a-real-model"

result = call_with_fallback(
    client,
    settings,
    "Reply with exactly: ok",
)
print(result)