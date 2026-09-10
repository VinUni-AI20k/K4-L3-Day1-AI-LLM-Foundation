"""
Checkpoint 4 (12h50) — Part 4: Mini-project run_assistant
Chạy:  pytest tests/test_part4.py -v
    Nhóm cơ bản:   pytest tests/test_part4.py -k Basic -v
    Nhóm kịch bản: pytest tests/test_part4.py -k Scenario -v
Tất cả API đều được mock — không cần API key thật.
"""

import unittest
from unittest.mock import MagicMock, patch

from tests._loader import MOD

REQUIRED_KEYS = {"num_turns", "total_tokens", "total_cost", "history"}


def _make_stream(text: str):
    """Tạo mock stream: cắt text thành các chunk giống OpenAI streaming."""
    chunks = []
    for piece in (text[: len(text) // 2], text[len(text) // 2 :]):
        chunk = MagicMock()
        chunk.choices = [MagicMock()]
        chunk.choices[0].delta.content = piece
        chunks.append(chunk)
    final = MagicMock()
    final.choices = [MagicMock()]
    final.choices[0].delta.content = None
    chunks.append(final)
    return chunks


class TestRunAssistantBasic(unittest.TestCase):

    def test_function_exists_and_is_callable(self):
        self.assertTrue(callable(MOD.run_assistant))

    @patch("openai.OpenAI")
    def test_quit_immediately_returns_stats_dict(self, MockOpenAI):
        MockOpenAI.return_value = MagicMock()
        get_input = MagicMock(side_effect=["quit"])

        result = MOD.run_assistant("Bạn là trợ lý.", get_input=get_input)

        self.assertIsInstance(result, dict)
        for key in REQUIRED_KEYS:
            self.assertIn(key, result, f"Thiếu key: {key}")
        self.assertEqual(result["num_turns"], 0)

    @patch("openai.OpenAI")
    def test_exit_is_case_insensitive(self, MockOpenAI):
        MockOpenAI.return_value = MagicMock()
        get_input = MagicMock(side_effect=["EXIT"])

        result = MOD.run_assistant("Bạn là trợ lý.", get_input=get_input)

        self.assertEqual(result["num_turns"], 0)

    @patch("openai.OpenAI")
    def test_max_turns_zero_returns_without_reading_input(self, MockOpenAI):
        MockOpenAI.return_value = MagicMock()
        get_input = MagicMock(side_effect=[])  # nếu bị gọi sẽ raise StopIteration

        result = MOD.run_assistant("Bạn là trợ lý.", get_input=get_input, max_turns=0)

        self.assertEqual(result["num_turns"], 0)


class TestRunAssistantScenario(unittest.TestCase):
    """Demo tự động: kịch bản hội thoại nhiều lượt có script."""

    PERSONA = "Bạn là trợ giảng thân thiện của khóa AI."

    def _run_conversation(self, MockOpenAI, user_messages, replies):
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.side_effect = [
            _make_stream(reply) for reply in replies
        ]
        get_input = MagicMock(side_effect=list(user_messages) + ["quit"])
        result = MOD.run_assistant(self.PERSONA, get_input=get_input)
        return result, mock_client

    @patch("openai.OpenAI")
    def test_two_turns_counted_and_stats_positive(self, MockOpenAI):
        result, _ = self._run_conversation(
            MockOpenAI,
            ["Xin chào", "Kể một sự thật thú vị"],
            ["Chào bạn, mình giúp gì được?", "Việt Nam có hơn 3000 km bờ biển."],
        )
        self.assertEqual(result["num_turns"], 2)
        self.assertGreater(result["total_tokens"], 0)
        self.assertGreater(result["total_cost"], 0.0)

    @patch("openai.OpenAI")
    def test_api_called_with_stream_and_persona(self, MockOpenAI):
        _, mock_client = self._run_conversation(
            MockOpenAI, ["Xin chào"], ["Chào bạn!"]
        )
        self.assertTrue(mock_client.chat.completions.create.called)
        _, kwargs = mock_client.chat.completions.create.call_args
        self.assertTrue(kwargs.get("stream", False), "Phải gọi API với stream=True")
        messages = kwargs.get("messages", [])
        system_contents = [m["content"] for m in messages if m["role"] == "system"]
        self.assertTrue(
            any(self.PERSONA in c for c in system_contents),
            "Persona phải được gửi làm system prompt",
        )

    @patch("openai.OpenAI")
    def test_history_contains_last_turn(self, MockOpenAI):
        result, _ = self._run_conversation(
            MockOpenAI,
            ["Câu hỏi thứ nhất", "Câu hỏi thứ hai"],
            ["Trả lời thứ nhất.", "Trả lời thứ hai."],
        )
        history_text = " ".join(m["content"] for m in result["history"])
        self.assertIn("Câu hỏi thứ hai", history_text)
        self.assertIn("Trả lời thứ hai", history_text)

    @patch("openai.OpenAI")
    def test_history_trimmed_to_three_turns(self, MockOpenAI):
        user_messages = [f"Câu hỏi số {i}" for i in range(1, 6)]  # 5 lượt
        replies = [f"Trả lời số {i}." for i in range(1, 6)]
        result, _ = self._run_conversation(MockOpenAI, user_messages, replies)

        self.assertEqual(result["num_turns"], 5)
        self.assertLessEqual(
            len(result["history"]),
            6,
            "History phải được cắt còn tối đa 3 lượt (6 message)",
        )

    @patch("openai.OpenAI")
    def test_max_turns_limits_conversation(self, MockOpenAI):
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.side_effect = [
            _make_stream(f"Trả lời {i}") for i in range(10)
        ]
        # Không có 'quit' — phiên phải tự dừng nhờ max_turns
        get_input = MagicMock(side_effect=[f"Câu {i}" for i in range(10)])

        result = MOD.run_assistant(self.PERSONA, get_input=get_input, max_turns=2)

        self.assertEqual(result["num_turns"], 2)


if __name__ == "__main__":
    unittest.main()
