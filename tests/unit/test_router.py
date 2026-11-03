
from types import SimpleNamespace

import pytest

from clauselens.llm import router


class FakeAPIError(Exception):
    def __init__(self, code):
        self.code = code
        super().__init__(f"API error {code}")


class FakeCache:
    def __init__(self):
        self.data = {}

    def make_key(self, model, prompt, system_instruction):
        return f"{model}:{prompt}:{system_instruction}"

    def get(self, key):
        return self.data.get(key)

    def put(self, key, value):
        self.data[key] = value


@pytest.fixture
def settings():
    return SimpleNamespace(
        primary_model="primary-model",
        backup_model="backup-model",
        max_retries=2,
        retry_base_wait_s=0,
        retry_max_wait_s=0,
        request_timeout_s=30,
        gemini_api_key=SimpleNamespace(
            get_secret_value=lambda: "fake-key"
        ),
    )


@pytest.fixture
def cache():
    return FakeCache()


@pytest.fixture
def result():
    return router.LLMResult(
        text='{"rent": 25000}',
        model="primary-model",
        input_tokens=100,
        output_tokens=50,
        thought_tokens=10,
        latency_s=0.5,
    )


def test_cache_hit_skips_gemini(monkeypatch, settings, cache, result):
    key = cache.make_key("primary-model", "prompt", None)
    cache.put(key, result.__dict__)

    def should_not_call(*args, **kwargs):
        pytest.fail("Gemini should not be called on a cache hit")

    monkeypatch.setattr(router, "call_gemini", should_not_call)

    output = router.call_with_retry(
        None, settings, "primary-model", "prompt", cache
    )

    assert output == result


def test_successful_call_is_cached(monkeypatch, settings, cache, result):
    monkeypatch.setattr(
        router, "call_gemini", lambda *args: result
    )

    output = router.call_with_retry(
        None, settings, "primary-model", "prompt", cache
    )

    key = cache.make_key("primary-model", "prompt", None)

    assert output == result
    assert cache.get(key) == result.__dict__


def test_retry_on_temporary_error(monkeypatch, settings, cache, result):
    monkeypatch.setattr(router.errors, "APIError", FakeAPIError)

    calls = {"count": 0}

    def fake_call(*args):
        calls["count"] += 1

        if calls["count"] < 3:
            raise FakeAPIError(503)

        return result

    monkeypatch.setattr(router, "call_gemini", fake_call)
    monkeypatch.setattr(router.time, "sleep", lambda _: None)

    output = router.call_with_retry(
        None, settings, "primary-model", "prompt", cache
    )

    assert output == result
    assert calls["count"] == 3


def test_non_retryable_error_is_raised(monkeypatch, settings, cache):
    monkeypatch.setattr(router.errors, "APIError", FakeAPIError)

    def fake_call(*args):
        raise FakeAPIError(400)

    monkeypatch.setattr(router, "call_gemini", fake_call)

    with pytest.raises(FakeAPIError):
        router.call_with_retry(
            None, settings, "primary-model", "prompt", cache
        )


def test_fallback_to_backup_model(monkeypatch, settings, cache, result):
    monkeypatch.setattr(router.errors, "APIError", FakeAPIError)

    calls = []

    def fake_call(client, model, prompt, system_instruction):
        calls.append(model)

        if model == "primary-model":
            raise FakeAPIError(404)

        return result

    monkeypatch.setattr(router, "call_gemini", fake_call)

    output = router.call_with_fallback(
        None, settings, "prompt", cache
    )

    assert calls == ["primary-model", "backup-model"]
    assert output == result


def test_fallback_preserves_system_instruction(
    monkeypatch, settings, cache, result
):
    monkeypatch.setattr(router.errors, "APIError", FakeAPIError)

    calls = []

    def fake_call(client, model, prompt, system_instruction):
        calls.append((model, system_instruction))

        if model == "primary-model":
            raise FakeAPIError(404)

        return result

    monkeypatch.setattr(router, "call_gemini", fake_call)

    router.call_with_fallback(
        None, settings, "prompt", cache, "Extract lease facts."
    )

    assert calls == [
        ("primary-model", "Extract lease facts."),
        ("backup-model", "Extract lease facts."),
    ]


def test_no_fallback_for_non_retryable_error(
    monkeypatch, settings, cache
):
    monkeypatch.setattr(router.errors, "APIError", FakeAPIError)

    calls = []

    def fake_call(client, model, prompt, system_instruction):
        calls.append(model)
        raise FakeAPIError(400)

    monkeypatch.setattr(router, "call_gemini", fake_call)

    with pytest.raises(FakeAPIError):
        router.call_with_fallback(
            None, settings, "prompt", cache
        )

    assert calls == ["primary-model"]
