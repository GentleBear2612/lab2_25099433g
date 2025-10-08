import io
import sys
import pytest

from src.llm import translate


def test_translate_no_token_raises_runtimeerror(monkeypatch):
    # Ensure env token is not set
    monkeypatch.delenv('GITHUB_TOKEN', raising=False)

    with pytest.raises(RuntimeError):
        translate("hello", target_language="French")


def test_translate_with_fake_token(monkeypatch, monkeypatchascontext):
    # If we don't want to call external API, we can patch call_llm_model
    from src import llm

    def fake_call(model, messages, temperature=0.2, top_p=1.0, api_token=None):
        return "Bonjour"

    monkeypatch.setattr(llm, 'call_llm_model', fake_call)
    result = translate("hello", target_language="French", api_token="fake-token")
    assert result == "Bonjour"
