"""質問スクリプトのテスト（Gemini APIは呼び出さない）。"""

import weakref
from types import SimpleNamespace

from app import ask as ask_module


def test_interactive_mode_reuses_chat_for_follow_up_questions(monkeypatch, capsys):
    class FakeChat:
        def __init__(self):
            self.questions = []
            self.client_ref = None

        def send_message(self, question):
            assert self.client_ref() is not None
            self.questions.append(question)
            return SimpleNamespace(text=f"回答: {question}", usage_metadata=None)

    class FakeClient:
        def __init__(self):
            self.chat = FakeChat()
            self.chat.client_ref = weakref.ref(self)

            class Chats:
                def create(inner_self, *, model):
                    assert model == ask_module.MODEL
                    return self.chat

            self.chats = Chats()

    chats = []

    def create_client(**kwargs):
        client = FakeClient()
        chats.append(client.chat)
        return client

    monkeypatch.setattr(ask_module.genai, "Client", create_client)
    questions = iter(["最初の質問", "それについて詳しく", "終了"])
    monkeypatch.setattr("builtins.input", lambda _: next(questions))
    monkeypatch.setattr("sys.argv", ["app.ask"])

    ask_module.main()

    output = capsys.readouterr().out
    assert chats[0].questions == ["最初の質問", "それについて詳しく"]
    assert "回答: 最初の質問" in output
    assert "回答: それについて詳しく" in output


def test_question_argument_keeps_single_question_mode(monkeypatch, capsys):
    monkeypatch.setattr(ask_module, "ask", lambda question: f"回答: {question}")
    monkeypatch.setattr("sys.argv", ["app.ask", "LoRAとは？"])

    ask_module.main()

    output = capsys.readouterr().out
    assert "[質問] LoRAとは？" in output
    assert "回答: LoRAとは？" in output
