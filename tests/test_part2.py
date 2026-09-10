"""
Checkpoint 2 (11h20) — Part 2: System prompt & token
Chạy:  pytest tests/test_part2.py -v
Tất cả API đều được mock — không cần API key thật.
count_tokens dùng tiktoken thật (hoặc fallback) — test chỉ kiểm tra tính chất.
"""

import unittest
from unittest.mock import MagicMock, patch

from tests._loader import MOD


def _make_openai_response(text: str = "Hello from OpenAI"):
    choice = MagicMock()
    choice.message.content = text
    resp = MagicMock()
    resp.choices = [choice]
    return resp


class TestChatWithSystemPrompt(unittest.TestCase):

    @patch("openai.OpenAI")
    def test_returns_tuple_str_float(self, MockOpenAI):
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_openai_response("OK")

        result = MOD.chat_with_system_prompt("Bạn là giáo viên.", "Chào bạn")

        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], str)
        self.assertIsInstance(result[1], float)
        self.assertGreater(result[1], 0.0)

    @patch("openai.OpenAI")
    def test_messages_contain_system_and_user_roles(self, MockOpenAI):
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_openai_response()

        system_prompt = "Bạn là chuyên gia lịch sử Việt Nam."
        user_prompt = "Nhà Trần có bao nhiêu đời vua?"
        MOD.chat_with_system_prompt(system_prompt, user_prompt)

        _, kwargs = mock_client.chat.completions.create.call_args
        messages = kwargs.get("messages")
        self.assertIsNotNone(messages, "Phải truyền messages= vào create()")
        roles = [m["role"] for m in messages]
        self.assertIn("system", roles)
        self.assertIn("user", roles)

    @patch("openai.OpenAI")
    def test_system_prompt_content_is_sent(self, MockOpenAI):
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.return_value = _make_openai_response()

        system_prompt = "PERSONA_DAC_BIET_XYZ"
        MOD.chat_with_system_prompt(system_prompt, "Câu hỏi")

        _, kwargs = mock_client.chat.completions.create.call_args
        system_contents = [
            m["content"] for m in kwargs.get("messages", []) if m["role"] == "system"
        ]
        self.assertTrue(
            any(system_prompt in c for c in system_contents),
            "Nội dung system_prompt phải nằm trong message role='system'",
        )


class TestCountTokens(unittest.TestCase):

    def test_returns_positive_int_for_non_empty_text(self):
        result = MOD.count_tokens("Xin chào Việt Nam")
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)

    def test_longer_text_has_more_tokens(self):
        short = MOD.count_tokens("word " * 10)
        long = MOD.count_tokens("word " * 200)
        self.assertGreater(long, short)

    def test_unknown_model_falls_back_gracefully(self):
        # Model lạ không được làm hàm crash — phải dùng ước lượng dự phòng
        result = MOD.count_tokens("some text here", model="khong-ton-tai-123")
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)


class TestEstimateCost(unittest.TestCase):

    PROMPT = "Hãy kể cho tôi một sự thật thú vị về Việt Nam. " * 5
    RESPONSE = "Việt Nam là nước xuất khẩu cà phê lớn thứ hai thế giới. " * 5

    def test_returns_dict_with_required_keys(self):
        result = MOD.estimate_cost(self.PROMPT, self.RESPONSE)
        required_keys = {
            "input_tokens",
            "output_tokens",
            "input_cost",
            "output_cost",
            "total_cost",
        }
        self.assertIsInstance(result, dict)
        for key in required_keys:
            self.assertIn(key, result, f"Thiếu key: {key}")

    def test_token_counts_are_positive_ints(self):
        result = MOD.estimate_cost(self.PROMPT, self.RESPONSE)
        self.assertIsInstance(result["input_tokens"], int)
        self.assertIsInstance(result["output_tokens"], int)
        self.assertGreater(result["input_tokens"], 0)
        self.assertGreater(result["output_tokens"], 0)

    def test_total_equals_input_plus_output(self):
        result = MOD.estimate_cost(self.PROMPT, self.RESPONSE)
        self.assertAlmostEqual(
            result["total_cost"],
            result["input_cost"] + result["output_cost"],
            places=10,
        )

    def test_mini_is_cheaper_than_gpt4o(self):
        cost_4o = MOD.estimate_cost(self.PROMPT, self.RESPONSE, model="gpt-4o")
        cost_mini = MOD.estimate_cost(self.PROMPT, self.RESPONSE, model="gpt-4o-mini")
        self.assertLess(cost_mini["total_cost"], cost_4o["total_cost"])


if __name__ == "__main__":
    unittest.main()
